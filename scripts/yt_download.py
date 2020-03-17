import os
import sys

APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP_PATH)

from src import tools
from src.api import youtube
import configargparse
import os
import pandas as pd

abs_path = os.path.dirname(os.path.abspath(__file__))
rel_path = 'outputs'
save_path = os.path.join(abs_path, '..', rel_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)

p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv, creates a json instead')
p.add('-a', '--amount', default=200, help='amount of entries to retrieve, default 200')
p.add('-s','--skip', default=0, help='amount of entries to skip, default 0')
p.add('--personal', default='',
      help='download personal data with your ID, must specify a token for your ytTREX user which can be retrieved by clicking on your extension icon.')
p.add('--last', dest='last', action='store_true', default=False,
      help='the last 60 contributions received by the community. It is cached for 2 minutes, the first request after cache expires would define the next 60.')
p.add('--video', default='',
      help='it takes the id from a YouTube url, e.g. (https://www.youtube.com/watch?v=)4-VLmhQSzr8, and returns data containing all the different related videos observed when the same videoId have been watched by ytTREX contributors. Maximum 110 evidences are returned.')
p.add('--related', default='',
      help='it takes the id from a YouTube url, and retrieves data about all the times a videoId was in the related list of other videos, so you can see where videoId was suggested.')
p.add('--personal_related', default='',
      help='it takes the id from a YouTube url, and retrieves data about all the times a videoId was in the related list of other videos, so you can see where videoId was suggested.')

config = vars(p.parse_args())


def save(df, path):
    if config['csv']:
        print('Saving CSV to ' + path + '.csv')
        df.to_csv(tools.uniquePath(path + '.csv'), index=False)
    else:
        print('Saving JSON to ' + path + '.json')
        with open(tools.uniquePath(path + '.json'),"wb") as f:
            f.write(df)


def expand(df):
    df = df.rename(columns={"title": "sourceTitle", "videoId": "sourceVideoId"})

    df2 = pd.DataFrame(columns=df.columns)
    df2_index = 0
    for row in df.iterrows():
        one_row = row[1]
        for list_value in row[1]["related"]:
            one_row["related"] = list_value
            df2.loc[df2_index] = one_row
            df2_index += 1

    df2[list(df2["related"].head(1).tolist()[0].keys())] = df2["related"].apply(
        lambda x: pd.Series([x[key] for key in x.keys()]))

    df = df2.rename(columns={"viz": "related_viz",
                             "vizstr": "related_vizstr",
                             "displayTime": "related_displayTime",
                             "expandedTime": "related_expandedTime",
                             "index": "related_index",
                             "videoId": "related_videoId",
                             "source": "related_source",
                             "title": "related_title",
                             "duration": "related_duration",
                             "timeago": "related_timeago"
                             })

    df = df.drop('related', 1)
    df = pd.concat([df.drop(['likeInfo'], axis=1), df['likeInfo'].apply(pd.Series)], axis=1)
    df = pd.concat([df.drop(['viewInfo'], axis=1), df['viewInfo'].apply(pd.Series)], axis=1)
    return df


def last():
    path = config['path'] + '/yt/last/last'
    if config['csv']:
        df = youtube.last()
        df = expand(df)
    else:
        df = youtube.last_json()
    save(df, path)


def personal():
    path = config['path'] + '/yt/personal/' + config['personal']
    if config['csv']:
        df = youtube.personal(config['personal'])
    else:
        df = youtube.personal_json(config['personal'])
    save(df, path)


def personal_related():
    path = config['path'] + '/yt/personal_related/' + config['personal_related']
    if config['csv']:
        df = youtube.personal_related(config['personal_related'])
    else:
        df = youtube.personal_related_json(config['personal_related'])
    save(df, path)


def video():
    path = config['path'] + '/yt/video/' + config['video']
    if config['csv']:
        df = youtube.video(config['video'])
        df = expand(df)
    else:
        df = youtube.video_json(config['video'])
    save(df, path)


def related():
    path = config['path'] + '/yt/related/' + config['related']
    if config['csv']:
        df = youtube.related(config['related'])
        df = expand(df)
    else:
        df = youtube.related_json(config['related'])
    save(df, path)


def main():
    if config['last']:
        last()
        return

    elif config['personal'] != '':
        personal()
        return

    elif config['video'] != '':
        video()
        return

    elif config['related'] != '':
        related()
        return

    elif config['personal_related'] != '':
        personal_related()
        return

    print('No output type specified, please specify an argument among: --last, --personal, --video, --related.')


if __name__ == "__main__":
    main()
