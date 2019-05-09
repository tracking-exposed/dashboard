import pandas as pd
from lib import API, tools
from lib.config import config
import datetime

df = API.getDf(config['token'], 'summary', config['amount'], config['skip'])
df = tools.setDatetimeIndex(df)
maxDate = str(df.index.max())[:-6]
minDate = str(df.index.min())[:-6]

timelines = df.timeline.unique()

total = pd.to_timedelta(0)

for t in timelines:
    ndf = tools.filter(t, df=df, what='timeline', kind='or')
    timespent = ndf.index.max() - ndf.index.min()
    total += timespent

n = 3
top = df.source.value_counts().nlargest(n)
nature = df.nature.value_counts()
percentage = str((nature.sponsored/nature.organic)*100)[:-12]+'%'

timeads = (total.seconds)*(nature.sponsored/nature.organic)

print('Information for timeframe: '+minDate+' to '+maxDate)
print('Total time spent on Facebook: '+str(total))
print('Top '+str(n)+' sources of information are: \n'+top.to_string())
print(percentage+' of the posts are sponsored posts.')
print('You spent an estimate of '+str(datetime.timedelta(seconds=(timeads)))[:-7]+' watching ads on Facebook.')