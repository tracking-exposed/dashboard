from lib import API, tools
from lib.config import config

def main():

        if config['name'] != None:
            path = config['path'] + '/' + config['name'] + '_summary'
        else:
            path = config['path'] + '/' + config['token'] + '_summary'

        df = API.getDf(config['token'], 'summary', config['amount'], config['skip'])

        if config['csv']:
            print('Saving CSV to '+path+ '.csv')
            df.to_csv(tools.uniquePath(path + '.csv'), index=False)
        if config['json']:
            print('Saving JSON to '+path + '.json')
            df.to_json(tools.uniquePath(path + '.json'))

if __name__ == "__main__":
    main()


'''
def getStatus():

    if config['name'] != None:
        path = config['path'] + '/' + config['name']
    else:
        path = config['path'] + '/' + config['token']

    df = API.getDf(config['token'], apiname='stats', count=config['amount'])
    # print(df)

    df= df[['startTime', 'impressionOrder']].groupby('startTime', as_index=True).max()
    df = tools.setDatetimeIndexFloor(df, what=config['granularity']).groupby(df.index).sum()

    if config['csv']:
        df.to_csv(path+'_status.csv')
    elif config['json']:
        df.to_json(path+'_status.json')
    else:
        print(df.to_string())
        
        '''