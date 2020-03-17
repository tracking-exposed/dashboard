'''
This libray allows to get data from the youtube.tracking.exposed API
and transforms it into pandas DataFrames. It implements caching and timeout.
'''

import requests
import pandas as pd
import requests_cache
import os
from src.errors import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# absolute path
script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
rel_path = "../.apicache/yttrex.db"
strCache = os.path.join(script_dir, rel_path)

# Initialize Caching
requests_cache.install_cache(backend='sqlite', expire_after=600, cache_name=strCache)

def personal(yttrexToken, server='https://youtube.tracking.exposed', amount=200, skip=0):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/'+str(amount)+'-'+str(skip)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    try:
        df = pd.DataFrame.from_records(data.json()['recent'])
    except KeyError:
        raise EmptyDataframeError('Error! Are you sure you used the correct yttrexToken?')
    checkDf(df)
    return df

def personal_json(yttrexToken, server='https://youtube.tracking.exposed', amount=200, skip=0):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/'+str(amount)+'-'+str(skip)
    print("Downloading data via", url)
    data = requests.get(url, verify=False).content
    return data

def video(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/videoId/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    # checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def video_json(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/videoId/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False).content
    return data


def related(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/related/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json())
    checkDf(df)
    return df

def related_json(videoId,server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/related/' + str(videoId)
    print("Downloading data via", url)
    data = requests.get(url, verify=False).content
    return data

def last(server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/last/'
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    df = pd.DataFrame.from_records(data.json()['content'])
    checkDf(df)
    return df

def last_json(server='https://youtube.tracking.exposed'):
    url = server + '/api/v1/last/'
    print("Downloading data via", url)
    data = requests.get(url, verify=False).content
    return data

def personal_related(yttrexToken, server='https://youtube.tracking.exposed', amount=200, skip=0):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/related/'+str(amount)+'-'+str(skip)
    print("Downloading data via", url)
    data = requests.get(url, verify=False)
    checkData(data)
    try:
        df = pd.DataFrame.from_records(data.json())
    except KeyError:
        raise EmptyDataframeError('Error! Are you sure you used the correct yttrexToken?')
    checkDf(df)
    return df

def personal_related_json(yttrexToken, server='https://youtube.tracking.exposed', amount=200, skip=0):
    url = server + '/api/v1/personal/' + str(yttrexToken)+'/related/'+str(amount)+'-'+str(skip)
    print("Downloading data via", url)
    data = requests.get(url, verify=False).content
    return data