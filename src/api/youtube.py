'''
This libray allows to get data from the youtube.tracking.exposed API
and transforms it into pandas DataFrames. It implements caching and timeout.
'''

import requests
import pandas as pd
import requests_cache
import os
from src.errors import *

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
rel_path = "../.apicache/yttrex.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)


'''
Keeping the functions separated allows to have human-readable code, and can be more specific.
The functions use requests with a cache in order to pull data from the tracking.exposed API,
converts it to pandas DataFrame cleans the data and returns the object.
'''

def personal(yttrexToken, server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/personal/' + str(yttrexToken)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    try:
        df = pd.DataFrame.from_records(data.json()['recent'])
    except KeyError:
        raise EmptyDataframeError('Error! Are you sure you used the correct yttrexToken?')
    checkDf(df)
    return df

def video(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/videoId/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    # checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def related(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/related/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def last(server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/last/'
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json()['content'])
    checkDf(df)
    return df

def personal_related(yttrexToken, server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/related'
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    try:
        df = pd.DataFrame.from_records(data.json())
    except KeyError:
        raise EmptyDataframeError('Error! Are you sure you used the correct yttrexToken?')
    checkDf(df)
    return df
