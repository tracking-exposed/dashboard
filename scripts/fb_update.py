import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)

import datetime, itertools, configargparse
import pandas as pd
from pathlib import Path
from src.api import facebook
import numpy as np

abs_path = os.path.dirname(os.path.dirname(__file__))
OUTPUTS = os.path.join(abs_path, 'outputs')
START_DATE = datetime.datetime.today() - datetime.timedelta(days=7000)
# Hierarchical Configuration
p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--token', help='token of your fbtrex user')
group.add_argument('-u', '--users_csv',
                   help='csv with name,token')
p.add('-n', '--name', help='name for your facebook profile, if using -t option')
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-p', '--path', help='path to save to (default "outputs")', default=OUTPUTS)
p.add('-s', '--start', help='start date. default: all data. format: MM/DD/AAAA',
      default=START_DATE)
p.add('--apiname', help='name of the API: summary, enrich, .. default: summary', default='summary')
p.add('--platform', help='name of the platform: fb for facebook, yt for youtube, .. default: fb', default='fb')

config = vars(p.parse_args())


def formatStop(stop_date):
    if type(stop_date) is not datetime.datetime:
        if len(stop_date) == 25:
            stop_date = datetime.datetime.strptime(
                stop_date, "%Y-%m-%d %H:%M:%S+00:00").timestamp()
            stop_date = pd.Timestamp(stop_date, unit='s').tz_localize('UTC')
            return stop_date
        elif len(stop_date) == 24:
            stop_date = datetime.datetime.strptime(
                stop_date, "%Y-%m-%dT%H:%M:%S.fZ").timestamp()
            stop_date = pd.Timestamp(stop_date, unit='s').tz_localize('UTC')
            return stop_date
        else:
            stop_date = pd.Timestamp(stop_date, unit='s').tz_localize('UTC')
            return stop_date
    else:
        stop_date = pd.Timestamp(stop_date, unit='s').tz_localize('UTC')
        return stop_date


def stopDate(token, apiname, platform):
    file = config['path'] + '/fb/' + apiname + '/' + token + '.csv'
    df = pd.read_csv(file, nrows=1)
    try:
        stop_date = df.iloc[0, 0]
        stop_date = formatStop(stop_date)
        return stop_date

    except IndexError or ValueError:
        print('Csv file is empty, using start_date from config.')
        stop_date = config['start']
        stop_date = formatStop(stop_date)
        return stop_date


def fileExists(token, apiname, platform):
    my_file = Path(config['path'] + '/fb/' + apiname + '/' + token + '.csv')
    return my_file.is_file()


def emptyCsv(token, apiname, platform):
    if apiname == 'summary' and platform == 'fb':
        df = pd.DataFrame(
            columns=['impressionTime', 'impressionOrder', 'semanticId', 'semanticCount', 'opengraph', 'id', 'user',
                     'timeline', 'publicationTime', 'postId', 'permaLink', 'fblinktype', 'nature', 'images',
                     'displaySource', 'source', 'sourceLink', 'texts', 'textsize', 'LIKE', 'HAHA', 'LOVE',
                     'videoautoplay', 'ANGRY', 'SAD', 'WOW'])
        df = df.set_index('impressionTime')

    elif apiname == 'enrich' and platform == 'fb':
        df = pd.DataFrame(columns=['impressionTime', 'impressionOrder', 'semanticId', 'semanticCount',
                                   'opengraph', 'user', 'timeline', 'publicationTime', 'postId',
                                   'permaLink', 'fblinktype', 'nature', 'images', 'displaySource',
                                   'source', 'sourceLink', 'texts', 'textsize', 'LIKE', 'LOVE', 'ANGRY',
                                   'labels', 'lang', 'WOW', 'SAD', 'HAHA', 'videoautoplay'])
        df = df.set_index('impressionTime')

    elif apiname == 'stats' and platform == 'fb':
        df = pd.DataFrame(columns=['startTime', 'geoip', 'impressionOrder', 'impressionTime', 'htmlId',
                                   'timelineId', 'summary'])

    df.to_csv(config['path'] + '/fb/' + apiname + '/' + token + '.csv')


def prepare(token=config['token'], apiname=config['apiname'], platform=config['platform']):
    if not fileExists(token, apiname, platform):
        print('file does not exist')
        emptyCsv(token, apiname, platform)

    df = pd.read_csv(config['path'] + '/fb/' + apiname + '/' + token + '.csv')

    return df


def clean(df):
    df.impressionTime = df.impressionTime.replace('', np.nan)
    df = df.dropna(subset=['impressionTime'])

    df['impressionTime'] = pd.to_datetime(df['impressionTime'], utc=True)
    df = df.set_index('impressionTime')
    if config['apiname'] == 'enrich':
        df = df.drop_duplicates('semanticId')
    elif config['apiname'] == 'stats':
        df = df.drop_duplicates('htmlId')
    else:
        df = df.drop_duplicates('id')

    df = df.sort_index(ascending=False)
    return df


def update(token=config['token'], apiname=config['apiname'], platform=config['platform'], limit=200):
    df = prepare(token, apiname, platform)

    stop = stopDate(token, apiname, platform)

    for i in itertools.count():

        try:
            if config['apiname'] == 'summary':
                df_temp = facebook.summary(token, count=limit, skip=i * limit)

            elif config['apiname'] == 'enrich':
                df_temp = facebook.enrich(token, count=limit, skip=i * limit)

            elif config['apiname'] == 'stats':
                limit = 1
                df_temp = facebook.stats(token, count=limit, skip=i * limit)
        except:
            break

        try:
            df_temp['impressionTime'] = pd.to_datetime(df_temp['impressionTime'], utc=True)
        except:
            continue

        earliest_date_for_chunk = min(df_temp['impressionTime'])
        len_of_chunk = len(df_temp.index)
        df = df.append(df_temp, sort=True)

        if earliest_date_for_chunk < stop:
            # stop
            print('Reached last date of csv')
            break

        elif len_of_chunk < limit:
            # stop
            print('Reached end of data')
            break

        elif earliest_date_for_chunk >= stop:
            continue

    df = clean(df)
    return df


def save(token=config['token'], apiname=config['apiname'], platform=config['platform']):
    update(token, apiname, platform).to_csv(config['path'] + '/fb/' + apiname + '/' + token + '.csv')
    return


def main():
    if config['users_csv'] != None:
        users = pd.read_csv(config['users_csv'])
        for index, row in users.iterrows():
            print('Checking ' + row['name'])
            save(row['token'])
    else:
        save()


if __name__ == '__main__':
    main()
