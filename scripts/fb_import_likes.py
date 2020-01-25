import pandas as pd
import os
from flatten_json import flatten
import json
import configargparse
from pandas.io.json import json_normalize


'''
Warning: this script uses a json copy of data from the facebook archive that you can download from your profile,
follow this help guide for more information: https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav
'''

p = configargparse.ArgParser()
p.add('-i', '--input', help='The path to the folder that contains all the unzipped Facebook "Your Data" json archives.', required=True)
p.add('-o', '--output', help='The path to the output folder, default is outputs/fb/your_data.',
      default='outputs/fb/your_data/')
config = vars(p.parse_args())


def filePaths(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith("posts_and_comments.json"):
                yield (os.path.join(root, file))


def postsAndComments(file):
    with open(file) as f:
        data = dict(json.load(f))
        data = (flatten(d) for d in data['reactions'])
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.columns = ['timestamp', 'reaction', 'actor', 'title']
        user = df.actor.iloc[0]
        print('Processing user: '+user)
        df["title"] = df["title"].str.replace(user+" likes ", "")
        df["title"] = df["title"].str.replace(user+" reacted to ", "")
        df['source'] = df.title.str.split("'s", expand=True)[0]
        df = df[~df['source'].str.contains('liked')]
        df = df[~df['source'].str.contains(' own post.')]
        df = df.set_index(df['timestamp'])
        df = df[['reaction', 'actor', 'source']]
    return df, user


def pages(file, user):
    with open(file) as f:
        data = dict(json.load(f))
        try:
            df = json_normalize(data['page_likes'])
            df['reaction'] = 'page_liked'
            df['actor'] = user
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df = df.set_index(df['timestamp'])
            df = df[['reaction', 'actor', 'name']]
            df.columns = ['reaction', 'actor', 'source']
        except KeyError:
            pass
    return df


def main():
    files = filePaths(config['input'])
    for file in files:
        likes_posts_and_comments, user = postsAndComments(file)
        likes_pages = pages(file.replace('posts_and_comments', 'pages'), user)
        frames = [likes_pages, likes_posts_and_comments]
        df = pd.concat(frames, sort=True).sort_index(ascending=False)
        save_path = config['output'] + 'likes_' + user.replace(" ", "_") + '.csv'
        df.to_csv(save_path)
        print('Saved to: ' + save_path)


if __name__ == '__main__':
    main()