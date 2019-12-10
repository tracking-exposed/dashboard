'''
This libray allows to get data from the facebook.tracking.exposed API
and transforms it into pandas DataFrames. It implements caching and timeout.
'''

import requests
import pandas as pd
import requests_cache
import os
from src.errors import *


script_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "../.apicache/fbtrex.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)

def clean(df):

    """
    Often (all the times?) only some reactions are calculated.
    We fill them with zeroes so we can work on an int type column.
    """

    df = df.fillna(value={'ANGRY': 0, 'HAHA': 0, 'LIKE': 0, 'LOVE': 0, 'SAD': 0, 'WOW': 0, 'videoautoplay': ''})
    return df


'''
Keeping the functions separated allows to have human-readable code, and can be more specific.
The functions use requests with a cache in order to pull data from the tracking.exposed API,
converts it to pandas dataframe, cleans the data and returns the object.
'''

def summary(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):
    apiname = 'summary'
    checkId(fbtrexToken)
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)
    data = requests.get(url, timeout=10)  # call API
    checkData(data)
    df = pd.DataFrame.from_records(data.json())  # convert to df
    checkDf(df)
    df = clean(df)
    return df


def enrich(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):

    apiname = 'enrich'
    checkId(fbtrexToken)
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)
    data = requests.get(url, timeout=10)    # call API
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    df = clean(df)
    return df

def stats(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):

    apiname = 'stats'
    checkId(fbtrexToken)
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)
    data = requests.get(url, timeout=10)    # call API
    checkData(data)
    df = pd.DataFrame.from_records(data.json()['content'])
    checkDf(df)
    return df