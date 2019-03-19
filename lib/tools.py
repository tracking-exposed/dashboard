import pandas as pd
from datetime import datetime
import os
# register converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# load configuration
from config import config

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
# NOTE: THIS IS INTENDED TO BE USED ONLY WITH PROFILES THAT ARE MAKING USE OF THE AUTOSCROLLING TAMPERMONKEY SCRIPT.
def doImpressionCount(df, timelinelist):
    maxlist = [] # generates list of impressionCount
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
    return data

# Filters Dataframe with start and end date. needs a datetime indexed dataframe
# You can set start and end with formats "yyyy-mm-dd" or "yyyy-mm-dd hh:mm:ss"
def setTimeframe(df, start):
    data = df.loc[start:]
    return data

def saveHtml(df):
    # save
    script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = "./local/" + config['name'] + ".html"
    strFile = os.path.join(script_dir, rel_path)
    # make sure file is overwritten
    if os.path.isfile(strFile):
        os.remove(strFile)
    return df.to_html(strFile)
