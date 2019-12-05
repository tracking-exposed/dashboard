from urllib.parse import urlencode
import urllib.request
from lib import API, tools
import configargparse
from datetime import datetime
import pandas as pd
import logging
import os
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


if config['name'] != None:
    path = config['path'] + '/' + config['name']+'.log'
elif config['token'] != None:
    path = config['path'] + '/' + config['token']+'.log'
elif config['users_csv'] != None:
    path = config['path'] + '/'+'multiple_users.log'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=path)

url = "https://api.telegram.org/bot" + config['telegram_token'] + "/sendMessage"

def spam(text):
    args = {}
    args['chat_id'] = config['channel_id']
    args['text'] = text
    post_data = urlencode(args)
    request = urllib.request.Request(url, bytearray(post_data, 'utf-8'))
    response = urllib.request.urlopen(request)
    return response


def check(username, token):
    df = API.getFacebook(token, apiname='stats', count=1, skip=0)

    # Check for parser errors
    parsing_errors = len(df.loc[(df.summary.astype(str) == '[]') & -(df.htmlId.isnull())])

    logging.info('Looking for errors for '+username+".")

    if parsing_errors > 0:
        logging.warning(username + ' encountered ' + str(parsing_errors) + ' parsing errors.')

    # Check if the bot is down
    delta = datetime.utcnow() - pd.to_datetime(df.startTime.max()).tz_localize(None)
    if delta.total_seconds() / 3600 > 1:
        logging.critical(username + ' is DOWN since ' + str(delta))
        spam('🚨 '+username + ' CRITICAL\n\n Down since ' + str(delta)[:-7])

    # Check if bot is correctly getting impressions
    max_impression_order = df.impressionOrder.max()
    if max_impression_order < 20:
        logging.error(username + ' has ' + str(max_impression_order) + ' impressions collected in the last hour.')
        spam(username + ' WARNING\n\n' + str(max_impression_order) + ' impressions in 1 hour.')


def main():
    if config['users_csv'] != None:
        users = pd.read_csv(config['users_csv'])
        for index, row in users.iterrows():
            print('Checking '+row['name']+'  --  token: '+ row['token'])
            check(row['name'], row['token'])

    elif config['name'] != None:
        check(config['name'], config['token'])

    else:
        check(config['token'], config['token'])

if __name__ == "__main__":
    main()