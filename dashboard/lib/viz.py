import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from lib.config import config

# gets dataframe and returns a plot
def impressionCount(df):
    ax = plt.subplot(111) # sets alignment of the plot
    barWidth = 0.01 # sets width of bars in the bar chart
    ax.bar(df.index, df.impressions, width=barWidth, align='edge') # creates the figure
    ax.xaxis_date() #sets x axis as datetime axis
    ax.set_title('Impression Count for '+config['name']) # sets the title
    ax.grid() # enables grid
    del df
    del ax
    return plt

def formatDates(plt):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M')) # formatting dates
    plt.setp(plt.gca().xaxis.get_majorticklabels(), 'rotation', 30, 'fontsize', 6) # makes dates readable
    return plt

# saves daily impressions needs timelineChart output
def savePng(plt, name):
    rel_path = name+".png"
    strFile = os.path.join(config['path'], rel_path)
    print('Saving to \'' + strFile + '\'')
    # make sure file is overwritten
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)
    return plt.clf()
