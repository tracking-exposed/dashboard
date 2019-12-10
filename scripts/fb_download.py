import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)

from src import tools
from src.api import facebook
from src.config import p
import pandas as pd

p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv, creates a json instead')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--apiname', default='summary', help='api name. should be summary, enrich or stats')
config = vars(p.parse_args())


def save(df, path):
    if config['csv']:
        print('Saving CSV to ' + path + '.csv')
        df.to_csv(tools.uniquePath(path + '.csv'), index=False)
    if not config['csv']:
        print('Saving JSON to ' + path + '.json')
        df.to_json(tools.uniquePath(path + '.json'))


def save_path(apiname):
    if config['name'] != None:
        path = config['path'] + '/fb/' + apiname + '/' + config['name']
    else:
        path = config['path'] + '/fb/' + apiname + '/' + config['token']
    return path


def stats_slow(token):
    limit = 1
    df = pd.DataFrame()
    for i in range(1, int(config['amount'])):
        df_temp = facebook.stats(token, count=limit, skip=config['skip'] + i * limit)
        df = df.append(df_temp, sort=True)
    df = df.drop_duplicates('htmlId')
    return df


def main(apiname=config['apiname']):
    path = save_path(apiname)

    if apiname == 'summary':
        df = facebook.summary(config['token'], config['amount'], config['skip'])
    elif apiname == 'enrich':
        df = facebook.enrich(config['token'], config['amount'], config['skip'])
    elif apiname == 'stats':
        df = stats_slow(config['token'])

    save(df, path)


if __name__ == '__main__':
    main()
