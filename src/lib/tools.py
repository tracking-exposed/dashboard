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
            sb = df[(df[what].str.contains(flt))]
            return sb
        else:
            raise ValueError('kind not recognized')