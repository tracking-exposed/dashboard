import pandas as pd
import os
from pandas.io.json import json_normalize
import json
import configargparse

'''
Warning: this script uses a json copy of data from the facebook archive that you can download from your profile,
follow this help guide for more information: https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav
'''

p = configargparse.ArgParser()
p.add('-i', '--input', help='The path to the folder that contains all the unzipped Facebook "Your Data" json archives.',
      required=True)
p.add('-o', '--output', help='The path to the output folder, default is outputs/fb/your_data.',
      default='outputs/fb/your_data/')
config = vars(p.parse_args())

def filePaths(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith("pages.json"):
                # print(os.path.join(root, file))
                yield (os.path.join(root, file))

files = filePaths(config['input'])
df_list = []

for file in files:
    with open(file) as f:
        data = dict(json.load(f))
        user = file.split('facebook-')[1].split('/')[0]
        try:
            df = json_normalize(data['page_likes'])
            df['reaction'] = 'page_liked'
            df['actor'] = user
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df = df.set_index(df['timestamp'])
            df = df[['name', 'reaction', 'actor']]
            df.columns = ['source', 'reaction', 'actor']
            save_path = config['output'] + user + '_pages' + '.csv'
            df.to_csv(save_path)
            print('Saved to: ' + save_path)
        except KeyError:
            pass

        # try:
        #     df = json_normalize(data['pages_followed'])
        # except KeyError:
        #     pass
        # try:
        #     df = json_normalize(data['pages_unfollowed'])
        # except KeyError:
        #     pass
        # pd.
        # print(data['page_likes'])
        # data = data['page_likes']
        # data = (flatten(d) for d in data)
        # print(data)
        # data =
        # print(dict(data))
        # df = pd.DataFrame(data)
        # print(df)

        # df.columns = ['timestamp', 'reaction', 'actor', 'title']
        # user = df.actor.iloc[0].split(" ")[0]
        # print('Processing user: '+user)
        # df["title"] = df["title"].str.replace(user+" likes ", "")
        # df["title"] = df["title"].str.replace(user+" reacted to ", "")
        # df['source'] = df.title.str.split("'s", expand=True)[0]
        # df = df[~df['source'].str.contains('liked')]
        # df = df[~df['source'].str.contains(' own post.')]

