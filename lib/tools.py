import pandas as pd
from datetime import datetime
# register converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# load configuration
# from config import config

# reads pandas dataframe from getSummary output
# returns list of unique timeline ids for the dataset
def doTimelineList(df):
    timelineList = []
    for index, row in df.iterrows():
        id = row['timeline']
        if not id in timelineList:
            timelineList.append(id)
        else:
            pass
    return timelineList


# reads pandas dataframe and a list of timeline ids (output from function getTimelineList)
# returns a dataframe with datetimeindex and impressionCount
def doImpressionCount(df, timelinelist):
    maxlist = []
    dateslist = []
    df2 = pd.DataFrame()
    for timeline in timelinelist:
        df2 = df[df['timeline'] == timeline]
        maxim = df2.impressionOrder.values.max()
        maxlist.append(maxim)
        minim = df2.impressionTime.values.min()
        dateslist.append(datetime.strptime(minim, '%Y-%m-%dT%H:%M:%S.%fZ'))
    del df2
    results = list(zip(dateslist, maxlist))
    data = pd.DataFrame(results, columns=['time', 'impressions'])
    data.set_index('time', inplace=True)
    return data

# Filters Dataframe since start of last $days days. needs a datetime indexed dataframe
def setTimeframe(df, start, end):
    df = df.loc[start:end]
    return df



