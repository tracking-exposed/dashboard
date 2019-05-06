import pandas as pd
from lib import API, tools
from lib.config import config
import datetime

df = tools.setDatetimeIndex(API.getDf(config['token'], 'summary', config['amount'], config['skip']))
max = str(df.index.max())[:-6]
min = str(df.index.min())[:-6]

timelines = df.timeline.unique()
total = pd.to_timedelta(0)

for t in timelines:
    ndf = tools.filter(t, df=df, what='timeline', kind='or')
    timespent = ndf.index.max() - ndf.index.min()
    total += timespent

n = 3
top = df.source.value_counts().nlargest(n)
nature = df.nature.value_counts()
perc = (str((nature.sponsored/nature.organic)*100)[:-12]+'%')

timeads = (total.seconds/100)*(nature.sponsored/nature.organic)*100

print('Information for timeframe: '+min+' to '+max)
print('Total time spent on Facebook: '+str(total))
print('Top '+str(n)+' sources of information are: \n'+top.to_string())
'''
We can show this as table in ipython:
    from IPython.display import display, HTML
    display(HTML(df.to_html()))
    '''

print(perc+' of the posts are sponsored posts.')
print('You spent an estimate of '+str(datetime.timedelta(minutes=(timeads/60)))[:-7]+' watching ads on Facebook.')

