import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from config import config

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
    # save
    script_dir = os.path.dirname(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = "./local/"+name+".png"
    strFile = os.path.join(script_dir, rel_path)
    # make sure file is overwritten
    if os.path.isfile(strFile):
        os.remove(strFile)
    plt.savefig(strFile)
    plt.clf()
