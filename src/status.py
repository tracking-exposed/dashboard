from lib import API, tools
from lib.config import config
from datetime import datetime, timezone, timedelta
import pandas as pd
import logging

logging.basicConfig(level=logging.WARNING, format='%(name)s - %(levelname)s - %(message)s')

if config['name'] != None:
    path = config['path'] + '/' + config['name']
else:
    path = config['path'] + '/' + config['token']

def checkBots():
    df = API.getDf(config['token'], apiname='stats', count=1, skip=0)
    # print(df)

    # Check for parser errors
    parsing_errors = len(df.loc[(df.summary.astype(str) == '[]') & -(df.htmlId.isnull())])
    if parsing_errors > 0:
        logging.warning('Encontered ' + str(parsing_errors) + ' parsing errors.')

    # Check if the bot is down
    delta = datetime.utcnow() - pd.to_datetime(df.startTime.max()).tz_localize(None)
    if delta.seconds / 3600 > 1:
        logging.critical('Warning, ' + config['name'] + ' is down since ' + str(delta))

    # Check if bot is correctly getting impressions
    max_impressionOrder = df.impressionOrder.max()
    if max_impressionOrder < 35:
        logging.error('Warning, ' + config['name'] + ' is having problems, only ' + str(max_impressionOrder) + ' impressions collected in the last hour.')


if __name__ == "__main__":
    checkBots()

