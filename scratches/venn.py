import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)
from src import tools
from matplotlib_venn import venn3
from matplotlib import pyplot as plt
import configargparse
import datetime
import os
import pandas as pd

# set up directory paths
abs_path = os.path.dirname(__file__)
rel_path = 'outputs'
save_path = os.path.join(abs_path, '..', rel_path)

# initialize configuration
p = configargparse.ArgParser(
)
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('--start', help='start date for harmonizer. default is since beginning',
      default=str(datetime.date.today() - datetime.timedelta(days=7000)))
p.add('-e', '--end', help='end date for harmonizer. default is today.', default=str(datetime.date.today()))
p.add('--sources', help='directory containing ONLY csv files from FBcrawl, used to merge with user data', required=True)
p.add('--user1', help='summary.csv file for user 1 that you want to compare', required=True)
p.add('--user2', help='summary.csv file for user 2 that you want to compare', required=True)
p.add('-s1', '--source1', help='string of the exact displayName for the first source', required=True)
p.add('-s2', '--source2', help='string of the exact displayName for the second source', required=True)
config = vars(p.parse_args())


def main():
    # Data Loading
    fbcrawl_output_files = [os.path.join(config['sources'], f) for f in os.listdir(config['sources']) if
                            os.path.isfile(os.path.join(config['sources'], f)) and f.endswith(
                                ".csv")]  # list of csv files (fbcrawl outputs) as input to be concatenated
    sources_data = tools.concatenateCsv(fbcrawl_output_files)  # concatenate csv
    user_a = pd.read_csv(config['user1'])
    user_b = pd.read_csv(config['user2'])

    # Data Cleaning
    sources_data = sources_data.drop(['shared_from'], axis=1).rename({'post_id': 'postId'},
                                                                     axis='columns').drop_duplicates(['postId']).fillna(
        0)  # cleaning data
    sources_data['source'] = sources_data['source'].str.split(',').str[0]  # preventing errors
    user_a, user_b, sources_data = tools.harmonize(a=[user_a, user_b, sources_data], start=config['start'],
                                                   end=config['end'], source1=config['source1'],
                                                   source2=config['source2'])  # preparing datasets to be merged
    user_a = user_a.reset_index().drop_duplicates(['postId']).fillna(0)
    user_b = user_b.reset_index().drop_duplicates(['postId']).fillna(0)
    sources_data = sources_data.reset_index()  # reset the index to merge datasets on postid

    # Creating lists of postIds as inputs for the venn diagram
    list_a = user_a["postId"].astype(str).tolist()
    list_b = user_b['postId'].astype(str).tolist()
    list_source = sources_data['postId'].astype(str).tolist()

    # Create Venn diagram
    venn3([set(list_a), set(list_b), set(list_source)], set_labels=('User A', 'User B', 'sources'))
    plt.title('Posts seen vs not seen\n')

    # Save SVG file
    filename = tools.uniquePath(config['path'] + '/venn.svg')
    print('saving to ' + filename)
    plt.savefig(filename,
                orientation='portrait', format='svg',
                transparent=False)


if __name__ == "__main__":
    main()
