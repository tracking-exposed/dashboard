import os
import datetime
import requests
import requests_cache
import pandas as pd
from pathlib import Path
import itertools
import configargparse
abs_path = os.path.dirname(os.path.dirname(__file__))
rel_path = 'outputs'
save_path = os.path.join(abs_path, rel_path)

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "./.apicache/retrieved.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(
    backend='sqlite', expire_after=600, cache_name=strCache)

# Hierarchical Configuration

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--token', help='token of your fbtrex user')
group.add_argument('-u', '--users_csv',
                   help='csv with name,token for username,fbtrex token')

p.add('-n', '--name', help='name for your facebook profile, if using -t option')
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('-s', '--start', help='start date for harmonizer. default is a week ago',
      default=datetime.datetime.today()-datetime.timedelta(days=7000))
p.add('-e', '--end', help='end date for harmonizer. default is today.',
      default=datetime.date.today())
p.add('--no-csv', dest='csv', action='store_false', default=True,
      help='do not create a csv, creates a json instead')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--apiname', help='name of the API: summary, semantics, .. default: summary', default='summary')
p.add('--no-labels', dest='labels', action='store_false',
      default=True, help='do not create a csv with labels')
config = vars(p.parse_args())

# Custom errors handling


class EmptyDataframeError(Exception):
    pass


def checkId(fbtrexToken):
    if (len(fbtrexToken) != 40):
        raise ValueError(
            'the fbtrexToken in configuration should be 40 characters long. This is '+str(len(fbtrexToken)))


def checkData(data):
    if (data.headers['Content-Type'] != 'application/json; charset=utf-8'):
        raise RuntimeError('Dataframe error')


def checkDf(df):
    if df.empty:
        raise EmptyDataframeError(
            'Dataframe is empty, are you sure you used the correct token/id?')
    elif type(df) == 'NoneType':
        raise EmptyDataframeError(
            'Dataframe is empty, are you sure you used the correct token/id?')


def get(fbtrexToken, apiname=config['apiname'], count=config['amount'], skip=config['skip'], server='facebook'):
    # check that fbtrexToken is correct
    checkId(fbtrexToken)
    server = 'https://'+server+'.tracking.exposed'
    # setup HTTP request
    url = server + '/api/v2/personal/' + \
        str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)

    # call API
    data = requests.get(url)

    # Check that Dataframe is not empty
    checkData(data)

    if apiname == 'summary':
        # convert to df
        df = pd.DataFrame.from_records(data.json())
        checkDf(df)
        return df.fillna(value={'ANGRY': 0, 'HAHA': 0, 'LIKE': 0, 'LOVE': 0, 'SAD': 0, 'WOW': 0, 'videoautoplay': ''})

    raise ValueError("Unsupported 'apiname' "+apiname)


def getLastDate(token, apiname):
    file = './outputs/'+token+'_'+apiname+'.csv'
    # df = get(token, count=1, skip=0)
    df = pd.read_csv(file, nrows=1)
    try:
        last_date = df.iloc[0, 0]
        # print(last_date)
        return last_date
    except IndexError or ValueError:
        print('Csv file is empty, using start_date from config.')
        return config['start']


def FileExists(token, apiname):
    my_file = Path('./outputs/'+token+'_'+apiname+'.csv')
    return my_file.is_file()


def CreateEmptyCsv(token, apiname):
    df = pd.DataFrame(columns=['impressionTime', 'impressionOrder', 'semanticId', 'semanticCount', 'opengraph', 'id', 'user',
                               'timeline', 'publicationTime', 'postId', 'permaLink', 'fblinktype', 'nature', 'images',
                               'displaySource', 'source', 'sourceLink', 'texts', 'textsize', 'LIKE', 'HAHA', 'LOVE',
                               'videoautoplay', 'ANGRY', 'SAD', 'WOW'])
    df = df.set_index('impressionTime')
    df.to_csv('./outputs/'+token+'_'+apiname+'.csv')


def stopDateN(stop_date):
    if type(stop_date) is not datetime.datetime:
        if len(stop_date) == len('2019-10-22 14:06:14+00:00'):
            stop_date_n = datetime.datetime.strptime(
                stop_date, "%Y-%m-%d %H:%M:%S+00:00").timestamp()
            return stop_date_n
        elif len(stop_date) == len('2019-11-08T09:05:22.000Z'):
            stop_date_n = datetime.datetime.strptime(
                stop_date, "%Y-%m-%dT%H:%M:%S.fZ").timestamp()
            return stop_date_n
    else:
        stop_date_n = stop_date
        return stop_date_n


def update(token=config['token'], apiname=config['apiname'], limit=200):

    if not FileExists(token, apiname=apiname):
        print('file does not exist')
        CreateEmptyCsv(token, apiname)

    # else:
    #     print('file exists!')

    stop_date = getLastDate(token, apiname)
    # print(type(stop_date))

    stop_date_n = stopDateN(stop_date)

    df = pd.read_csv('./outputs/'+token+'_'+apiname+'.csv')
    # print('stop date in n is :'+str(stop_date_n))
    for i in itertools.count():

        df_temp = get(token, apiname, count=limit, skip=i*limit)
        df_temp['impressionTime'] = pd.to_datetime(df_temp['impressionTime'],
                                                   # format='%d%b%Y:%H:%M:%S.%f'
                                                   )
        earliest_date_for_chunk = min(df_temp['impressionTime'])

        len_of_chunk = len(df_temp.index)
        # print('length of chunk number '+str(i)+' :'+str(len(df_temp.index)))
        # print('earliest date from chunk '+str(earliest_date_for_chunk))
        df = df.append(df_temp, sort=True)
        # add to csv
        stop = pd.Timestamp(stop_date_n, unit='s').tz_localize('UTC')
        # print('comparing earliest chunk date: ' +
        #       str(earliest_date_for_chunk)+' with stop: '+str(stop))
        if earliest_date_for_chunk < stop:
            # stop
            print('Reached last date of csv')
            break
        elif len_of_chunk < 200:
            # stop
            print('Reached end of data')
            break
        elif earliest_date_for_chunk >= stop:
            print('Chunk done, downloading next..')
            continue

    df['impressionTime'] = pd.to_datetime(df['impressionTime'], utc=True)
    df = df.set_index('impressionTime')
    df = df.drop_duplicates('id')
    # print(len(df))
    df = df.sort_index(ascending=False)
    return df


def update_it(token=config['token'], apiname=config['apiname']):
    df = update(token, apiname)
    df.to_csv('./outputs/'+token+'_'+apiname+'.csv')
    return


def main():
    if config['users_csv'] != None:
        users = pd.read_csv(config['users_csv'])
        for index, row in users.iterrows():
            print('Checking '+row['name'])
            update_it(row['token'])
    else:
        update_it()


if __name__ == '__main__':
    main()