import pandas as pd
import numpy as np
import sys

sys.path.append('..')
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

stats = pd.DataFrame(columns=['user', 'start', 'end',
                              'average_impression_count',
                              'timelines',
                              'total_entries',
                              'missing values'
                              ])


# def timeframe(df):
#     maxDate = str(df.impressionTime.max())
#     minDate = str(df.impressionTime.min())
#     return maxDate, minDate


def timeSpent(df):
    timelines = df.timeline.unique()
    total = pd.to_timedelta(0)

    for t in timelines:
        ndf = tools.filter(t, df=df, what='timeline', kind='or')
        timespent = ndf.index.max() - ndf.index.min()
        total += timespent
    return total


def topSources(df, n=10):
    top = df.source.value_counts().nlargest(n)
    return top


def sponsoredInfo(df):
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


def topPost(df, n=1):
    df = df[df['permaLink'] != '/ads/about']
    top = df.permaLink.value_counts().nlargest(n)
    return top


def myStats(df):
    user_list = df.user.unique()
    for user in user_list:
        data = df[(df['user'] == user)]
        n = 1
        # maxDate, minDate = getTimeframe(df)
        total = timeSpent(df)
        top = topSources(df, n=n)
        percentage, timeads = sponsoredInfo(df)
        top_post = topPost(df)

        print('Total time spent on Facebook: ' + str(total))
        print('Top ' + str(n) + ' sources of information are: \n' + top.to_string())
        print(percentage + ' of the posts are sponsored posts.')
        print('You spent an estimate of ' + timeads + ' watching ads on Facebook.')
        print('Top posts:')

        stats.loc[user] = [
            user,
            data.impressionTime.min(),
            data.impressionTime.max(),
            # max(df.impressionOrder),
            # min(df.groupby(['timeline'], sort=False)['impressionOrder'].max()),
            data.impressionOrder.mean(),
            data['timeline'].nunique(),
            data['id'].count(),
            data.isna().sum().sum()
        ]
    return stats


def table_tab(df):
    # Calculate summary stats for table

    stats = myStats(df)
    user_src = ColumnDataSource(stats)

    # Columns of table
    table_columns = [TableColumn(field='user', title='Username'),
                     TableColumn(field='start', title='Start'),
                     TableColumn(field='end', title='End'),
                     TableColumn(field='average_impression_count', title='Avg Impressions per Timeline'),
                     TableColumn(field='timelines', title='# of Timelines'),
                     TableColumn(field='total_entries', title='Total Entries'),
                     TableColumn(field='missing values', title='Missing Values')
                     ]

    user_table = DataTable(source=user_src,
                           columns=table_columns, width=1000)

    tab = Panel(child=user_table, title='Summary Table')

    return tab
