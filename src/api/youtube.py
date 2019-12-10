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

def personal(yttrexToken, server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/personal/' + str(yttrexToken)
    print("Downloading data via", url)
    # call API
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
    # call API
    data = requests.get(url, verify=False)
    # checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def related(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/related/' + str(videoId)
    print("Downloading data via", url)
    # call API
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def last(server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/last/'
    print("Downloading data via", url)
    # call API
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json()['content'])
    checkDf(df)
    return df

def personal_related(yttrexToken, server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/related'
    print("Downloading data via", url)
    # call API
    data = requests.get(url, verify=False)
    checkData(data)
    try:
        df = pd.DataFrame.from_records(data.json())
    except KeyError:
        raise EmptyDataframeError('Error! Are you sure you used the correct yttrexToken?')

    checkDf(df)
    return df
