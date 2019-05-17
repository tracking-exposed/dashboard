import pandas as pd
from lib import tools
import configargparse
import datetime
import os

abs_path = os.path.dirname(__file__)
print(abs_path)
rel_path = 'outputs'
save_path = os.path.join(abs_path, '..', rel_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)

p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('--start', help='start date for harmonizer. default is a week ago', default=str(datetime.date.today()-datetime.timedelta(days=7)))
p.add('-e', '--end', help='end date for harmonizer. default is tomorrow.', default=str(datetime.date.today()))
p.add('--sources', help='directory containing ONLY csv files from FBcrawl, used to merge with user data', required=True)
p.add('--users', help='directory containing ONLY csv files from fbtrex, used to merge with user data', required=True)
p.add('-s1', '--source1', help='string of the exact displayname for the first source', required=True)
p.add('-s2', '--source2', help='string of the exact displayname for the second source', required=True)
config = vars(p.parse_args())

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
        return df


# make sure list of dfs (summary or fbcrawl output) has same two sources and same timeframe,
# specified timeframe should be smaller than timeframe of the datasets otherwise doesn't work

def harmonize(a=[], # list of fbcrawl or fbtrex summary outputs
              start=config['start'], # start date as string UTC e.g. 2019-05-15
              end=config['end'], # end date as string UTC
              source1=config['source1'], # exact name of 'source', (the name displayed, not the @username)
              source2=config['source2']): # exact name of 'source'. (EU19 is intended to only compare two)

    # make dates machine readable
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)

    # cycle through the list of fbcrawl merged outputs and user
    for i in range(0, len(a)):

        if 'date' in a[i].columns: # if it's a fbcrawl output
            a[i] = a[i][(a[i]['date'].str.match('\d\d\d\d-\d\d-\d.*', na=True)) | a[i].date.notnull()] # filter out entries without a date
            a[i]['date'] = pd.to_datetime(a[i]['date'], utc=True) # converts date to datetime
            m = (a[i]['date'] >= start) & (a[i]['date'] <= end)
            a[i] = a[i].loc[m].set_index(['date']).sort_index()
            a[i] = tools.filter(source1, source2, df=a[i], what='source', kind='or')

        elif 'publicationTime' in a[i].columns: # if its a fbtrex output
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


def main():
    # Data Loading
    fbtrex_output_files = [os.path.join(config['users'], f) for f in os.listdir(config['users']) if os.path.isfile(os.path.join(config['users'], f)) and f.endswith(".csv")]
    user_data = concatenateCsv(fbtrex_output_files)

    fbcrawl_output_files = [os.path.join(config['sources'], f) for f in os.listdir(config['sources']) if os.path.isfile(os.path.join(config['sources'], f)) and f.endswith(".csv")] #list of csv files (fbcrawl outputs) as input to be concatenated
    sources_data = concatenateCsv(fbcrawl_output_files) # concatenate csv

    # Data Cleaning
    sources_data = sources_data.drop(['shared_from'], axis=1).rename({'post_id': 'postId'}, axis='columns').drop_duplicates(['postId']).fillna(0) # cleaning data
    sources_data['source'] = sources_data['source'].str.split(',').str[0] # preventing errors

    user_data = user_data
    user_data = user_data.drop(['ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW', 'displaySource',
       'fblinktype', 'images', 'impressionTime',
       'nature', 'opengraph', 'permaLink', 'semanticCount',
       'semanticId', 'sourceLink', 'texts', 'textsize', 'timeline'], axis=1).drop_duplicates(['id']).fillna(0)

    user_data, sources_data = harmonize([user_data, sources_data]) # preparing datasets to be merged

    f = {'id': 'count',
         'impressionOrder': 'mean',
         'user': lambda x: x.nunique()
         }

    df = user_data[['postId','id','impressionOrder','user']].groupby('postId').agg(f) # perform aggregations
    df = df.rename({'id': 'total_views', 'user': 'seen_by', 'impressionOrder':'average_order'}, axis='columns') # rename columns

    # reset the index to merge datasets on postid
    df = df.reset_index()
    sources_data = sources_data.reset_index()

    # merge the data and clean posts which were not seen on fbcrawl
    s = pd.merge(sources_data, df, on='postId', how='outer').fillna(0)
    s = s[s.date != 0]
    s = s.set_index(['date', 'postId'])
    path = config['path'] + '/combined.csv'
    s.to_csv(tools.uniquePath(path))

if __name__ == "__main__":
    main()