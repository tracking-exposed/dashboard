import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)

from urllib.parse import urlencode
import urllib.request
from src.api import facebook
import configargparse
from datetime import datetime
import pandas as pd
import logging

abs_path = os.path.dirname(os.path.dirname(__file__))
rel_path = 'outputs'
save_path = os.path.join(abs_path, rel_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--token', help='token of your fbtrex user')
group.add_argument('-u', '--users_csv', help='csv with name,token for username,fbtrex token')

p.add('-n', '--name', help='name for your facebook profile, if using -t option')
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('-i', '--channel_id', required=True, help='id or name of the channel')
p.add('-b', '--telegram_token', help='bot token', required=True)

config = vars(p.parse_args())
URL = "https://api.telegram.org/bot" + config['telegram_token'] + "/sendMessage"


def save_path():
    if config['name'] != None:
        path = config['path'] + '/' + config['name'] + '.log'
    elif config['token'] != None:
        path = config['path'] + '/' + config['token'] + '.log'
    elif config['users_csv'] != None:
        path = config['path'] + '/' + 'multiple_users.log'
    return path


def spam(text):
    args = {}
    args['chat_id'] = config['channel_id']
    args['text'] = text
    post_data = urlencode(args)
    request = urllib.request.Request(URL, bytearray(post_data, 'utf-8'))
    response = urllib.request.urlopen(request)
    return response


def has_parsing_errors(parsing_errors, threshold=1):
    if parsing_errors >= threshold:
        return True
    else:
        return False


def is_down(delta, seconds=3600):
    if delta.total_seconds() > seconds:
        return True
    else:
        return False


def gets_few_impressions(max_impression_order, threshold=20):
    if max_impression_order < threshold:
        return True
    else:
        return False


def check(username, token):
    path = save_path()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=path)

    df = facebook.stats(token, count=1, skip=0)
    parsing_errors = len(df.loc[(df.summary.astype(str) == '[]') & -(df.htmlId.isnull())])
    delta = datetime.utcnow() - pd.to_datetime(df.startTime.max()).tz_localize(None)
    max_impression_order = df.impressionOrder.max()

    logging.info('Looking for errors for ' + username + ".")

    if has_parsing_errors(parsing_errors):
        logging.warning(username + ' encountered ' + str(parsing_errors) + ' parsing errors.')

    if is_down(delta):
        logging.critical(username + ' is DOWN since ' + str(delta))
        spam('🚨 ' + username + ' CRITICAL\n\n Down since ' + str(delta)[:-7])

    # Check if bot is correctly getting impressions
    if gets_few_impressions(max_impression_order):
        logging.error(username + ' has ' + str(max_impression_order) + ' impressions collected in the last hour.')
        spam(username + ' WARNING\n\n' + str(max_impression_order) + ' impressions in 1 hour.')


def main():
    if config['users_csv'] != None:
        users = pd.read_csv(config['users_csv'])
        for index, row in users.iterrows():
            print('Checking ' + row['name'] + '  --  token: ' + row['token'])
            check(row['name'], row['token'])
    elif config['name'] != None:
        check(config['name'], config['token'])
    else:
        check(config['token'], config['token'])


if __name__ == "__main__":
    main()
