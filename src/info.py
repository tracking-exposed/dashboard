import pandas as pd
from lib import API, tools
from lib.config import p
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words
stop_words = get_stop_words('es')

p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--top', help='number of top sources to retrieve', default=10)
p.add('--wordcloud', dest='wordcloud', action='store_true', default=False, help='creates a wordcloud and opens it')
config = vars(p.parse_args())

df = API.getDf(config['token'], 'summary', config['amount'], config['skip'])
df = tools.setDatetimeIndex(df)

opengraph = pd.DataFrame.from_dict(df.opengraph.to_dict()).T

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
    total = getTimeSpent(df)
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

def getTopPosts(df, n=10):
    top = opengraph.title.value_counts().nlargest(n)
    return top

def generate_wordcloud(df): # optionally add: stopwords=STOPWORDS and change the arg below
    text = df.texts.str.join(sep=',').reset_index()
    text.columns = ['date', 'words']
    text = text.words.str.cat(sep=' ')

    wordcloud = WordCloud(font_path='src/DejaVuSans.ttf',
                          relative_scaling = 1.0,
                          stopwords = stop_words # set or space-separated string
                          ).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def main():
    maxDate, minDate = getTimeframe(df)
    total = getTimeSpent(df)
    top = getTopSources(df, n=n)
    percentage, timeads = getSponsoredInfo(df)

    print('Information for timeframe: ' + minDate + ' to ' + maxDate)
    print('Total time spent on Facebook: ' + str(total))
    print('Top ' + str(n) + ' sources of information are: \n' + top.to_string())
    print(percentage + ' of the posts are sponsored posts.')
    print('You spent an estimate of ' + timeads + ' watching ads on Facebook.')
    print('Most seen posts:')
    print(getTopPosts(df))

    if config['wordcloud']:
        generate_wordcloud(df)

if __name__ == '__main__':
    main()