from lib import API, tools
from lib.config import p
from datetime import datetime
import pandas as pd
import logging


config = vars(p.parse_args())


if config['name'] != None:
    path = config['path'] + '/' + config['name']+'.log'
    name = config['name']
else:
    path = config['path'] + '/' + config['token']+'.log'
    name = config['path']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=path)


def check():
    df = API.getDf(config['token'], apiname='stats', count=1, skip=0)

    # Check for parser errors
    parsing_errors = len(df.loc[(df.summary.astype(str) == '[]') & -(df.htmlId.isnull())])

    logging.info('Looking for errors for '+name)

    if parsing_errors > 0:
        logging.warning(name + ' encountered ' + str(parsing_errors) + ' parsing errors.')

    # Check if the bot is down
    delta = datetime.utcnow() - pd.to_datetime(df.startTime.max()).tz_localize(None)
    if delta.seconds / 3600 > 1:
        logging.critical(name + ' is DOWN since ' + str(delta))

    # Check if bot is correctly getting impressions
    max_impressionOrder = df.impressionOrder.max()
    if max_impressionOrder < 35:
        logging.error(name + ' is having problems, only ' + str(max_impressionOrder) + ' impressions collected in the last hour.')


if __name__ == "__main__":
    check()