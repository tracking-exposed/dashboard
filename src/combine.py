import pandas as pd
import numpy as np
from lib import API, tools
from lib.config import config
import os

# concatenates csvs together, takes paths as arguments.
# we only want to concatenate the sources
def concatenateCsv(list):
    df = pd.DataFrame()
    for a in list:
        try:
            if df.empty:
                df = pd.read_csv(a)
            else:
                df = df.append(pd.read_csv(a), ignore_index=True)
        except FileNotFoundError:
            print('File '+a+' not found.')
    if df.empty:
        raise ValueError('Empty dataframe. Reading sources failed.')
    else:
        return df.drop(['shared_from', 'url', 'text'], axis=1).rename({'post_id': 'postId'},axis='columns').drop_duplicates(['postId'])


# HARMONIZES DATES AND SOURCES FOR A LIST OF DATAFRAMES, must be summary or fbcrawl output
def harmonize(a=[], start=config['start'], end=config['end'], source1=config['source1'], source2=config['source2']):
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)

    for i in range(0, len(a)):
        if 'date' in a[i].columns:
            a[i] = a[i][(a[i]['date'].str.match('\d\d\d\d-\d\d-\d.*', na=True)) | a[i].date.notnull()]
            a[i]['date'] = pd.to_datetime(a[i]['date'], utc=True)
            m = (a[i]['date'] >= start) & (a[i]['date'] <= end)
            a[i] = a[i].loc[m].set_index(['date']).sort_index()
            a[i] = tools.filter(source1, source2, df=a[i], what='source', kind='or')
        elif 'publicationTime' in a[i].columns:
            a[i] = a[i][(a[i]['publicationTime'].str.match('\d\d\d\d-\d\d-\d.*', na=True)) | a[i].publicationTime.notnull()]
            a[i]['publicationTime'] = pd.to_datetime(a[i]['publicationTime'], utc=True)
            m = (a[i]['publicationTime'] >= start) & (a[i]['publicationTime'] <= end)
            a[i] = a[i].loc[m].set_index(['publicationTime']).sort_index().drop(['videoautoplay'], axis=1)
            if 'Unnamed: 0' in a[i].columns:
                a[i] = a[i].drop(['Unnamed: 0'], axis=1)
            a[i] = tools.filter(source1, source2, df=a[i], what='source', kind='or')
        else:
            raise ValueError('cannot find the dates column')
    return a

def mergeData(us, s):
    for i in range(0, len(us)):
        us[i] = pd.DataFrame(us[i]['postId'].value_counts()).reset_index()
        us[i] = us[i].rename({'postId': str(i) + '_count'}, axis='columns')
        us[i] = us[i].rename({'index': 'postId'}, axis='columns')
        s = s.reset_index()
        us[i]['postId'] = us[i]['postId'].astype(str).astype(int) # convert postId to be integer
        s = pd.merge(s, us[i], on='postId', how='outer').fillna(0)
        s[str(i) + '_seen'] = np.where(s[str(i) + '_count'] >= 1, 'yes', 'no')
    s = s[s.date != 0]
    s = s.set_index(['date'])
    return s

def main():
    a = API.getDf(config['token'], 'summary', config['amount'], config['skip'])
    files = [os.path.join(config['sources'], f) for f in os.listdir(config['sources']) if os.path.isfile(os.path.join(config['sources'], f)) and f.endswith(".csv")]
    s = concatenateCsv(files)
    s['source'] = s['source'].str.split(',').str[0] # preventing small errors
    a, s = harmonize([a, s])
    list = [a]
    df = mergeData(list, s).fillna(0)
    out = tools.uniquePath(config['path']+'/combined.csv')
    print('Saving output to '+out)
    df.to_csv(out)

if __name__ == "__main__":
    main()