import pandas as pd
import os
from datetime import datetime

now = datetime.now()
def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if str(f)[0] == '.':
                pass
            else:
                yield os.path.abspath(os.path.join(dirpath, f))

def source_count(df):
    source_count = pd.DataFrame(df.groupby(['user','nature','source'])['source'].count())
    source_count.columns = ['count']
    source_count = source_count.reset_index()
    return source_count

def post_count(df):
    df = df[df['permaLink'] != '/ads/about']

    # for each user get nlargest 50 or so
    post_count = pd.DataFrame(df.groupby(['user','source','texts','permaLink'])['permaLink'].count())
    post_count.columns = ['count']
    post_count = post_count.reset_index()
    for u in post_count.user.unique():
        mask = (post_count['user'] == u)
        post_count[mask] = post_count[mask].nlargest(50, 'count')
    post_count = post_count.dropna()
    return post_count

def posts_vs_ads(df):
    posts_vs_ads = pd.DataFrame(df.groupby(['user', 'nature'])['nature'].count())
    posts_vs_ads.columns = ['count']
    posts_vs_ads = posts_vs_ads.reset_index()
    posts_vs_ads = posts_vs_ads.pivot_table(values='count', index='user', columns='nature', aggfunc='first')
    return posts_vs_ads

def scrolling_time(df):
    posts_vs_ads_time = pd.DataFrame(columns=['time_spent'])
    for user in df.user.unique():
        data = df[df['user'] == user]
        data = data[['nature', 'user', 'impressionTime', 'timeline']]
        posts_vs_ads_time.loc[user] = [
            timeSpent(data)
        ]
    return posts_vs_ads_time


def timeSpent(df):
    timelines = df.timeline.unique()

    total = pd.to_timedelta(0)
    df['impressionTime'] = pd.to_datetime(df['impressionTime'])
    for t in timelines:
        data = df[df['timeline']==t]
        timespent = data.impressionTime.max() - data.impressionTime.min()
        total += timespent
    return total

folder = "./outputs/fb/summary/"
files = absoluteFilePaths(folder)

users = []
data = {}
for f in files:
    df = pd.read_csv(f)
    user = df.user.iloc[0].replace(" ","").lower()
    data.update({user: df})

df = pd.concat(data.values())
df['timestamp'] = pd.to_datetime(df['impressionTime']).astype(int)/1000000
print('Preparing posts_vs_ads.csv ...')
posts_vs_ads = posts_vs_ads(df)
print('Preparing scrolling_time.csv ...')
scrolling_time = scrolling_time(df)
print('Preparing source_count.csv ...')
source_count = source_count(df)
print('Preparing posts_count.csv ...')
post_count = post_count(df)

output_folder = './outputs/fb/aggregated/'
posts_vs_ads.to_csv(output_folder+'posts_vs_ads.csv')
scrolling_time.to_csv(output_folder+'scrolling_time.csv')
source_count.to_csv(output_folder+'source_count.csv')
post_count.to_csv(output_folder+'post_count.csv')

print('Elapsed time: {}'.format(str(datetime.now()-now)))
