import pandas as pd
from datetime import datetime
import os
# register converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# load configuration
# from config import config

# reads pandas dataframe from getSummary output
# returns list of unique timeline ids for the dataset
def makeList(df, what):
    newList = []
    for index, row in df.iterrows():
        id = row[str(what)]
        if not id in newList:
            newList.append(id)
        else:
            pass
    return newList

# reads pandas dataframe and a list of timeline ids (output from function getTimelineList)
# returns a dataframe with datetimeindex and impressionCount
# NOTE: THIS IS INTENDED TO BE USED ONLY WITH PROFILES THAT ARE MAKING USE OF THE AUTOSCROLLING TAMPERMONKEY SCRIPT.
def doImpressionCount(df, timelinelist):
    maxlist = [] # boot lists
    dateslist = [] #
    df2 = pd.DataFrame()
    for timeline in timelinelist: # we group all the impressions together for each timeline id
        df2 = df[df['timeline'] == timeline]  #create a new dataset filtered for a specific timeline id
        maxim = df2.impressionOrder.values.max() # the maximum number of impressionOrder is the number of impressions we have from that timeline
        maxlist.append(maxim) # adds the value to a list
        minim = df2.impressionTime.values.min() # gets the start time of the timeline scrolling (before refresh or next timeline use)
        dateslist.append(datetime.strptime(minim, '%Y-%m-%dT%H:%M:%S.%fZ'))
    del df2
    results = list(zip(dateslist, maxlist))
    data = pd.DataFrame(results,
                        columns=['time', 'impressions']
                        )
    data.set_index('time',
                   inplace=True
                   )
    data.sort_index()
    return data

def setDatetimeIndex(df, what):
    if what == 'publication':
        df = df.set_index(pd.DatetimeIndex(df['publicationTime']))
        return df
    elif what  == 'impression':
        df = df.set_index(pd.DatetimeIndex(df['impressionTime']))
        return df
    else:
        print('what should be either publication or impression.')
        raise ValueError

def setDatetimeIndexFloor(df, what):
    df.index = df.index.floor(what)
    return df

def doAggregation(df):
    # result = df[['user', 'timeline']].groupby(['user', 'timeline']).count()
    df = df.groupby(df.index).size()
    df = df.reset_index()
    df = df.set_index('impressionTime')
    return df

# Filters Dataframe with start and end date. needs a datetime indexed dataframe
# You can set start and end with formats "yyyy-mm-dd" or "yyyy-mm-dd hh:mm:ss"

def setTimeframe(df, start, end):
    data = df.loc[end:start]
    return data

def saveHtml(df, savename):
    # save
    script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = "./local/" + savename + ".html"
    strFile = os.path.join(script_dir, rel_path)
    # make sure file is overwritten
    if os.path.isfile(strFile):
        print('File already exists: overwriting.')
        os.remove(strFile)
    return df.to_html(strFile)

def filterTexts(df, search):
    sb = df[df['texts'].str.contains(search)]
    return sb
