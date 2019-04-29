import os ; import pandas as pd ; from pandas.plotting import register_matplotlib_converters ; register_matplotlib_converters() # register converters
# from lib.config import config

'''Takes a column, removes all the duplicates
    and returns a list of unique values.'''

def makeList(df, what):
    newList = []
    for index, row in df.iterrows():
        id = row[str(what)]
        if not id in newList:
            newList.append(id)
        else:
            pass
    return newList


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
        print('\"what\" should be either \"publication\" or \"impression\".')
        raise ValueError


'''Reduces datetime index from minimum values
    of milliseconds to hours (1H), or days (1D)'''

def setDatetimeIndexFloor(df, what):
    # df.index = pd.to_datetime(df.index)
    df.index = df.index.floor(what)
    return df


'''Returns an aggregated version of the Dataframe.
    After setting the floor, we count all the values with the same index.'''

def countImpressions(df):
    df = df.groupby(df.index).size()
    df = df.reset_index()
    df = df.set_index('impressionTime')
    df.columns = ['impressions']
    return df


'''Filters Dataframe with start and end date. needs a datetime indexed dataframe
    You can set start and end with formats "yyyy-mm-dd" or "yyyy-mm-dd hh:mm:ss"'''

def setTimeframe(df, start, end):
    df.sort_index(inplace=True, ascending=True)
    data = df.loc[start:end]
    return data


'''Saves dataframe to html table. Css styling
    and names can be added in the future.'''

# def saveHtml(df, savename):
#     # save
#     rel_path = savename + ".html"
#     strFile = os.path.join(config['path'], rel_path)
#     print('Saving to \'' + strFile + '\'')
#
#     # make sure file is overwritten
#     if os.path.isfile(strFile):
#         print('File already exists: overwriting.')
#         os.remove(strFile)
#
#     print('Done!')
#     return df.to_html(strFile)


'''Filters out the text column to get a Dataframe with impressions
    that contain a specific keyword or string.'''

def filter(df, what, search1, search2):
    flt = search1+'|'+search2
    sb = df[(df[what].str.contains(flt))]
    return sb

