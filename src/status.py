from lib import API, tools
from lib.config import status as config

def main():
    if config['name'] != None:
        path = config['path'] + '/' + config['name']
    else:
        path = config['path'] + '/' + config['token']

    df = API.getDf(config['token'], apiname='stats', count=config['amount'])[['startTime', 'impressionOrder']].groupby('startTime', as_index=True).max()
    df = tools.setDatetimeIndexFloor(df, what=config['granularity']).groupby(df.index).sum()

    if config['csv']:
        df.to_csv(path+'_status.csv')
    elif config['json']:
        df.to_json(path+'_status.json')
    else:
        print(df)

if __name__ == "__main__":
    main()