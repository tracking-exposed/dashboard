import requests
import pandas as pd
import requests_cache
import os
from src.errors import *

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
rel_path = "../.apicache/fbtrex.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)

def clean(df):
    df = df.fillna(value={'ANGRY': 0, 'HAHA': 0, 'LIKE': 0, 'LOVE': 0, 'SAD': 0, 'WOW': 0, 'videoautoplay': ''})
    return df


def summary(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):

    apiname = 'summary'

    #check that fbtrexToken is correct
    checkId(fbtrexToken)

    # setup HTTP request
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)

    data = requests.get(url)  # call API
    checkData(data)

    df = pd.DataFrame.from_records(data.json())  # convert to df
    checkDf(df)
    df = clean(df)
    return df


def enrich(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):

    apiname = 'enrich'
    #check that fbtrexToken is correct
    checkId(fbtrexToken)

    # setup HTTP request
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)
    # call API
    data = requests.get(url, timeout=10)

    # Check that Dataframe is not empty
    # checkData(data)
    # convert to df
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    df = clean(df)
    return df

def stats(fbtrexToken, count=400, skip=0, server='https://facebook.tracking.exposed'):

    apiname = 'stats'
    #check that fbtrexToken is correct
    checkId(fbtrexToken)

    # setup HTTP request
    url = server + '/api/v2/personal/' + str(fbtrexToken) + '/' + apiname + '/' + str(count) + '-' + str(skip)
    print("Downloading JSON data via", url)
    # call API
    data = requests.get(url)

    # Check that Dataframe is not empty
    checkData(data)

    df = pd.DataFrame.from_records(data.json()['content'])
    checkDf(df)
    return df



# raise ValueError("Unsupported 'apiname' "+apiname)