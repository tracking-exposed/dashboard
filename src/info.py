import pandas as pd
from lib import API, tools
from lib.config import p
import datetime

p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--top', help='number of top sources to retrieve', default=10)
config = vars(p.parse_args())

df = API.getDf(config['token'], 'summary', config['amount'], config['skip'])
df = tools.setDatetimeIndex(df)

n = int(config['top'])

def getTimeframe(df):
    maxDate = str(df.index.max())
    minDate = str(df.index.min())
    return maxDate, minDate

def getTimeSpent(df):
    timelines = df.timeline.unique()

    total = pd.to_timedelta(0)

    for t in timelines:
        ndf = tools.filter(t, df=df, what='timeline', kind='or')
        timespent = ndf.index.max() - ndf.index.min()
        total += timespent
    return total

def getTopSources(df, n=10):
    top = df.source.value_counts().nlargest(n)
    return top

def getSponsoredInfo(df):
    nature = df.nature.value_counts()
    try:
        percentage = (nature.sponsored/nature.organic)*100
    except AttributeError:
        percentage = 0

    if percentage == 0:
        result = "0%"
        timeads = '00:00:00'
    else:
        result = str(percentage)[:-12]+'%'
        timeads = (total.seconds) * float(result.strip('%')) / 100
        timeads = str(datetime.timedelta(seconds=(timeads)))[:-7]
    return result,timeads

def getUniqueSources(df, granularity='1D'):
    df = tools.setDatetimeIndexFloor(df, granularity)
    df = df.groupby(df.index)['source'].nunique()
    return df

maxDate, minDate = getTimeframe(df)
total = getTimeSpent(df)
top = getTopSources(df, n=n)
percentage, timeads = getSponsoredInfo(df)


print('Information for timeframe: '+minDate+' to '+maxDate)
print('Total time spent on Facebook: '+str(total))
print('Top '+str(n)+' sources of information are: \n'+top.to_string())
print(percentage+' of the posts are sponsored posts.')
print('You spent an estimate of '+timeads+' watching ads on Facebook.')

print(getUniqueSources(df))