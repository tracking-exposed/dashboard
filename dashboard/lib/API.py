import requests
import pandas as pd
import requests_cache
import os

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
rel_path = "./local/api-cache"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)

# Custom errors handling
class EmptyDataframeError(Exception):
    pass

def checkId(id):
    if (len(id) != 40):
        raise ValueError('the ID in configuration should be 40 characters long. This is '+str(len(id)))
        return
    else:
        return

def checkData(data):
    if (data.headers['Content-Type'] != 'application/json; charset=utf-8'):
        raise RuntimeError('Dataframe error')
        return
    else:
        return

def checkDf(df):
    if df.empty:
        raise EmptyDataframeError()
    elif type(df) == 'NoneType':
        raise EmptyDataframeError()
    else:
        return


'''calls (cached) api and returns json data.'''

def getDf(id, type='summary', count=2000, skip=0):

    #check that id is correct
    checkId(id)

    # setup HTTP request
    url = 'https://facebook.tracking.exposed/api/v2/personal/' + str(id) + '/' + type + '/' + str(count)+'-'+str(skip)
    print("Accessing summary, ID hidden.")

    # call API
    data = requests.get(url)

    # Check that Dataframe is not empty
    checkData(data)

    # convert to df
    df = pd.DataFrame.from_records(data.json())

    if type == 'summary':
        df = df.fillna(value={'ANGRY': 0, 'HAHA': 0, 'LIKE': 0, 'LOVE': 0, 'SAD': 0, 'WOW': 0, 'videoautoplay': ''})
        return df
    else:
        return df

    return df
