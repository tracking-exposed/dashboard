import pandas as pd
from pandas.plotting import register_matplotlib_converters ; register_matplotlib_converters() # register converters
import tempfile
import itertools as IT
import os

def uniquePath(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename

'''Sets the index as datetime, can be either
    by publicationTime or impressionTime'''

def setDatetimeIndex(df, what='impression'):
    if what == 'publication':
        df = df.set_index(pd.DatetimeIndex(df['publicationTime']))
        return df
    elif what  == 'impression':
        df = df.set_index(pd.DatetimeIndex(df['impressionTime']))
        return df
    else:
        raise ValueError('\"what\" should be either \"publication\" or \"impression\".')

'''Reduces datetime index from minimum values
    of milliseconds to hours (1H), or days (1D)
    default hour'''

def setDatetimeIndexFloor(df, what='1H'):
    df.index = pd.to_datetime(df.index)
    df.index = df.index.floor(what)
    return df

'''Filters Dataframe with start and end date. needs a datetime indexed dataframe
    You can set start and end with formats "yyyy-mm-dd" or "yyyy-mm-dd hh:mm:ss"'''

def setTimeframe(df, start, end):
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)
    df = df.loc[start:end]
    return df

'''Filters out the text column to get a Dataframe with impressions
    that contain a specific keyword or string.'''

def filter(*args, df, what, kind='or'):
    if args == []:
        raise ValueError('Please define at least one word argument to use as filter')
    else:
        if kind == 'or':
            flt = "|".join(args)
            sb = df[(df[what].str.contains(flt, na=False))]
            return sb
        else:
            raise ValueError('kind not recognized')

# make sure list of dfs (summary or fbcrawl output) has same two sources and same timeframe,
# specified timeframe should be smaller than timeframe of the datasets otherwise doesn't work

def harmonize(a, # list of fbcrawl or fbtrex summary outputs
              start, # start date as string UTC e.g. 2019-05-15
              end, # end date as string UTC
              source1, # exact name of 'source', (the name displayed, not the @username)
              source2): # exact name of 'source'. (EU19 is intended to only compare two)

    # make dates machine readable
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)

    # cycle through the list of fbcrawl merged outputs and user
    for i in range(0, len(a)):

        if 'date' in a[i].columns: # if it's a fbcrawl output
            a[i] = a[i][(a[i]['date'].str.match('\d\d\d\d-\d\d-\d.*', na=True)) | a[i].date.notnull()] # filter out entries without a date
            a[i]['date'] = pd.to_datetime(a[i]['date'], utc=True) # converts date to datetime
            m = (a[i]['date'] >= start) & (a[i]['date'] <= end) # filter for the timeframe
            a[i] = a[i].loc[m].set_index(['date']).sort_index() # filters out timeframe and sets sorted index
            a[i] = filter(source1, source2, df=a[i], what='source', kind='or')

        elif 'publicationTime' in a[i].columns: # if its a fbtrex output
            a[i] = a[i][(a[i]['publicationTime'].str.match('\d\d\d\d-\d\d-\d.*', na=True)) | a[i].publicationTime.notnull()]
            a[i]['publicationTime'] = pd.to_datetime(a[i]['publicationTime'], utc=True)
            m = (a[i]['publicationTime'] >= start) & (a[i]['publicationTime'] <= end)
            a[i] = a[i].loc[m].set_index(['publicationTime']).sort_index().drop(['videoautoplay'], axis=1)
            if 'Unnamed: 0' in a[i].columns:
                a[i] = a[i].drop(['Unnamed: 0'], axis=1)
            a[i] = filter(source1, source2, df=a[i], what='source', kind='or')

        else:
            raise ValueError('cannot find the dates column')
    return a

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
        return df