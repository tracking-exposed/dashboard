import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from datetime import timedelta
import os
import logging
import configargparse
from API import getSummary # imports API layer

# register converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# logging and error handling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# load configuration
p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
p.add('-n', '--name', help='arbitrary name for profile', required=True)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-i', '--id', help='id of your fbtrex user', required=True)
config = vars(p.parse_args())

# reads pandas dataframe from getSummary output
# returns list of unique timeline ids for the dataset
def getTimelineList(df):
    timelineList = []
    for index, row in df.iterrows():
        id = row['timeline']
        if not id in timelineList:
            timelineList.append(id)
        else:
            pass
    return timelineList


# reads pandas dataframe and a list of timeline ids (output from function getTimelineList)
# to get a tuple of values for impression count
def getTimelineData(df, timelinelist):
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
def setTimeframe(df, days):
    yesterday = datetime.now() - timedelta(days=days)
    startdate = datetime.strftime(yesterday.replace(hour=0, minute=0, second=0, microsecond=0), "%Y-%m-%d %H:%M:%S")
    df = df.loc[startdate:]
    return df, startdate


# gets dataframe and returns a plot
def makeTimelinePlot(df, startdate):
    ax = plt.subplot(111) # sets alignment of the plot
    barWidth = 0.02 # sets width of bars in the bar chart
    ax.bar(df.index, df.impressions, width=barWidth, align='edge') # creates the figure
    ax.xaxis_date() #sets x axis as datetime axis
    ax.set_title('Impression count for '+config['name']+' since '+str(startdate)) # sets the title
    ax.grid() # enables grid
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # formatting dates
    plt.setp(plt.gca().xaxis.get_majorticklabels(), 'rotation', 90) # makes dates readable
    del df
    del ax
    return plt

# defines routine to retrieve
def timelineChart(df):
    timelinelist = getTimelineList(df) #retrieves list of timeline ids for dataframe
    timelinedata = getTimelineData(df, timelinelist) # produces a dataframe with timeline startdates and impression count
    timeline, startdate = setTimeframe(timelinedata, days=0) # returns a filtered dataset
    chart = makeTimelinePlot(timeline,startdate) # produces a chart
    return chart

# saves daily impressions
def saveDailyImpressions(config):
    start = datetime.now()  # for testing purposes
    df = getSummary(config['id'])
    print('total impressions:'+str(len(df))) # for testing purposes
    end = (datetime.now()-start) # for testing purposes
    print(str(end)+' seconds to run the script') # for testing purposes
    del start
    del end
    chart = timelineChart(df)
    del df

    # save
    script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = "./local/last.png"
    strFile = os.path.join(script_dir, rel_path)
    # make sure file is overwritten
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)
    chart.savefig(strFile)
    plt.clf()
    chart.clf()
