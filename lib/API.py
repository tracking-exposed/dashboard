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

# calls api summary and returns a pandas dataframe. this could be generic when APIs are final
def getDF(id, type, count, skip):

    #check that id is correct
    checkId(id)

    # setup HTTP request
    url = 'https://testing.tracking.exposed/api/v2/personal/' + str(id) + '/' + type + '/' + str(count)+'-'+str(skip)
    print("Accessing summary, ID hidden.")

    # call API
    data = requests.get(url)

    # Check that Dataframe is not empty
    checkData(data)

    # convert to DataFrame
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df
