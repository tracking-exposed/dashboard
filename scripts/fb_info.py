import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)

import pandas as pd
from src import tools
import datetime
from stop_words import get_stop_words
import configargparse

stop_words = get_stop_words('es')
dashboard_folder = os.path.dirname(os.path.dirname(__file__))
outputs_relative_path = 'outputs'
SAVE_PATH = os.path.join(dashboard_folder, '.', outputs_relative_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)

p.add('-n', '--name', help='Name for your facebook profile.')
p.add('-t', '--token', help='Personal token for your facebook.tracking.exposed extension.', required=True)
p.add('-c', '--config', is_config_file=True, help='Configuration file. Check configargparse documentation for formats.')
p.add('-p', '--path', help='Path to save to (default: "outputs").', default=SAVE_PATH)
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--top', help='number of top sources to retrieve', default=10)
p.add('--wordcloud', dest='wordcloud', action='store_true', default=False, help='creates a wordcloud and opens it')
config = vars(p.parse_args())


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
        percentage = (nature.sponsored / nature.organic) * 100
    except AttributeError:
        percentage = 0

    if percentage == 0:
        result = "0%"
        timeads = '00:00:00'
    else:
        result = str(percentage)[:-12] + '%'
        timeads = (total.seconds) * float(result.strip('%')) / 100
        timeads = str(datetime.timedelta(seconds=(timeads)))[:-7]
    return result, timeads


def getTopPosts(df, n=10):
    df = df[df['permaLink'] != '/ads/about']
    top = df.permaLink.value_counts().nlargest(n)
    return top


def main():
    file = config['path'] + '/fb/summary/' + config['token'] + '.csv'
    df = pd.read_csv(file)
    df = tools.setDatetimeIndex(df)
    n = int(config['top'])
    maxDate, minDate = getTimeframe(df)
    total = getTimeSpent(df)
    top = getTopSources(df, n=n)
    percentage, timeads = getSponsoredInfo(df)
    top_posts = getTopPosts(df)

    print('Information for timeframe: ' + minDate + ' to ' + maxDate)
    print('Total time spent on Facebook: ' + str(total))
    print('Top ' + str(n) + ' sources of information are: \n' + top.to_string())
    print(percentage + ' of the posts are sponsored posts.')
    print('You spent an estimate of ' + timeads + ' watching ads on Facebook.')
    print('Top posts:')
    print(top_posts)


if __name__ == '__main__':
    main()
