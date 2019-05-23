import requests
import pandas as pd
import requests_cache
import os

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
rel_path = "../.apicache/retrieved.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)

# Custom errors handling
class EmptyDataframeError(Exception):
    pass

def checkId(fbtrexToken):
    if (len(fbtrexToken) != 40):
        raise ValueError('the fbtrexToken in configuration should be 40 characters long. This is '+str(len(fbtrexToken)))

def checkData(data):
    if (data.headers['Content-Type'] != 'application/json; charset=utf-8'):
        raise RuntimeError('Dataframe error')

def checkDf(df):
    if df.empty:
        raise EmptyDataframeError()
    elif type(df) == 'NoneType':
        raise EmptyDataframeError()


'''calls (cached) api and returns json data.'''
def getDf(fbtrexToken, apiname='summary', count=400, skip=0, server='https://facebook.tracking.exposed'):
    #check that fbtrexToken is correct
    checkId(fbtrexToken)

    # setup HTTP request
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url);
    # call API
    data = requests.get(url)

    # Check that Dataframe is not empty
    checkData(data)
    if apiname == 'summary' or apiname == 'semantics':
        # convert to df
        df = pd.DataFrame.from_records(data.json())
        checkDf(df)
        return df.fillna(value={'ANGRY': 0, 'HAHA': 0, 'LIKE': 0, 'LOVE': 0, 'SAD': 0, 'WOW': 0, 'videoautoplay': ''})
    elif apiname == 'stats':
        df = pd.DataFrame.from_records(data.json()['content'])
        checkDf(df)
        return df
    raise ValueError("Unsupported 'apiname' "+apiname)

