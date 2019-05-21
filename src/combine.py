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

def main():
    # Data Loading
    fbtrex_output_files = [os.path.join(config['users'], f) for f in os.listdir(config['users']) if os.path.isfile(os.path.join(config['users'], f)) and f.endswith(".csv")]
    user_data = tools.concatenateCsv(fbtrex_output_files)

    fbcrawl_output_files = [os.path.join(config['sources'], f) for f in os.listdir(config['sources']) if os.path.isfile(os.path.join(config['sources'], f)) and f.endswith(".csv")] #list of csv files (fbcrawl outputs) as input to be concatenated
    sources_data = tools.concatenateCsv(fbcrawl_output_files) # concatenate csv

    # Data Cleaning
    sources_data = sources_data.drop(['shared_from'], axis=1).rename({'post_id': 'postId'}, axis='columns').drop_duplicates(['postId']).fillna(0) # cleaning data
    sources_data['source'] = sources_data['source'].str.split(',').str[0] # preventing errors

    user_data = user_data
    user_data = user_data.drop(['ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW', 'displaySource',
       'fblinktype', 'images', 'impressionTime',
       'nature', 'opengraph', 'permaLink', 'semanticCount',
       'semanticId', 'sourceLink', 'texts', 'textsize', 'timeline'], axis=1).drop_duplicates(['id']).fillna(0)

    user_data, sources_data = tools.harmonize([user_data, sources_data],
                                              start=config['start'],
                                              end=config['end'],
                                              source1=config['source1'],
                                              source2=config['source2']
                                              ) # preparing datasets to be merged

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