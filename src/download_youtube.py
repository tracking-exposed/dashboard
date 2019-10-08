from lib import API, tools
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
p.add('--personal', default='', help='download personal data with your ID, must specify a token for your ytTREX user which can be retrieved by clicking on your extension icon.')
p.add('--last', dest='last', action='store_true', default=False, help='the last 60 contributions received by the community. It is cached for 2 minutes, the first request after cache expires would define the next 60.')
p.add('--video', default='', help='it takes the id from a YouTube url, e.g. (https://www.youtube.com/watch?v=)4-VLmhQSzr8, and returns data containing all the different related videos observed when the same videoId have been watched by ytTREX contributors. Maximum 110 evidences are returned.')
p.add('--related', default='', help='it takes the id from a YouTube url, and retrieves data about all the times a videoId was in the related list of other videos, so you can see where videoId was suggested.')
config = vars(p.parse_args())

def save(df, path):
    if config['csv']:
        print('Saving CSV to ' + path + '.csv')
        df.to_csv(tools.uniquePath(path + '.csv'), index=False)
    if not config['csv']:
        print('Saving JSON to ' + path + '.json')
        df.to_json(tools.uniquePath(path + '.json'))

def main():

        if config['last']:
            path = config['path'] + '/last'
            last = API.getLast()
            last = last.rename(columns={"title": "sourceTitle", "videoId": "sourceVideoId"})
            df2 = pd.DataFrame(columns=last.columns)
            df2_index = 0
            for row in last.iterrows():
                one_row = row[1]
                for list_value in row[1]["related"]:
                    one_row["related"] = list_value
                    df2.loc[df2_index] = one_row
                    df2_index += 1

            df2[list(df2["related"].head(1).tolist()[0].keys())] = df2["related"].apply(
                lambda x: pd.Series([x[key] for key in x.keys()]))

            last = df2.rename(columns={"viz": "related_viz",
                                           "vizstr": "related_vizstr",
                                           "displayTime": "related_displayTime",
                                           "expandedTime": "related_expandedTime",
                                           "index": "related_index",
                                           "videoId": "related_videoId",
                                           "source": "related_source",
                                           "title": "related_title",
                                           "duration": "related_duration",
                                           "timeago": "related_timeago",

                                           })
            last = last.drop('related', 1)
            last = pd.concat([last.drop(['likeInfo'], axis=1), last['likeInfo'].apply(pd.Series)], axis=1)
            last = pd.concat([last.drop(['viewInfo'], axis=1), last['viewInfo'].apply(pd.Series)], axis=1)
            save(last, path)

        if config['personal'] != '':
            path = config['path'] + '/personal'
            personal = API.getPersonal(config['personal'])

            personal = personal.rename(columns={"title": "sourceTitle", "videoId": "sourceVideoId"})

            df2 = pd.DataFrame(columns=personal.columns)
            df2_index = 0
            for row in personal.iterrows():
                one_row = row[1]
                for list_value in row[1]["related"]:
                    one_row["related"] = list_value
                    df2.loc[df2_index] = one_row
                    df2_index += 1

            df2[list(df2["related"].head(1).tolist()[0].keys())] = df2["related"].apply(
                lambda x: pd.Series([x[key] for key in x.keys()]))

            personal = df2.rename(columns={"longlabel": "related_longlabel",
                                     "vizstr": "related_vizstr",
                                     "displayTime": "related_displayTime",
                                     "expandedTime": "related_expandedTime",
                                     "index": "related_index",
                                     "videoId": "related_videoId",
                                     "source": "related_source",
                                     "title": "related_title"
                                     })
            personal = personal.drop('related', 1)
            personal = pd.concat([personal.drop(['likeInfo'], axis=1), personal['likeInfo'].apply(pd.Series)], axis=1)
            personal = pd.concat([personal.drop(['viewInfo'], axis=1), personal['viewInfo'].apply(pd.Series)], axis=1)
            save(personal, path)

        if config['video'] != '':
            path = config['path'] + '/'+config['video']+'_video'
            video = API.getVideo(config['video'])
            video = video.rename(columns={"title": "sourceTitle", "videoId": "sourceVideoId"})
            df2 = pd.DataFrame(columns=video.columns)
            df2_index = 0
            for row in video.iterrows():
                one_row = row[1]
                for list_value in row[1]["related"]:
                    one_row["related"] = list_value
                    df2.loc[df2_index] = one_row
                    df2_index += 1

            df2[list(df2["related"].head(1).tolist()[0].keys())] = df2["related"].apply(
                lambda x: pd.Series([x[key] for key in x.keys()]))

            video = df2.rename(columns={"viz": "related_viz",
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

            video = video.drop('related', 1)
            video = pd.concat([video.drop(['likeInfo'], axis=1), video['likeInfo'].apply(pd.Series)], axis=1)
            video = pd.concat([video.drop(['viewInfo'], axis=1), video['viewInfo'].apply(pd.Series)], axis=1)
            save(video, path)

        if config['related'] != '':
            path = config['path'] + '/'+config['related']+'_related'
            related = API.getRelated(config['related'])
            related = related.rename(columns={"title": "sourceTitle", "videoId": "sourceVideoId"})
            df2 = pd.DataFrame(columns=related.columns)
            df2_index = 0
            for row in related.iterrows():
                one_row = row[1]
                for list_value in row[1]["related"]:
                    one_row["related"] = list_value
                    df2.loc[df2_index] = one_row
                    df2_index += 1

            df2[list(df2["related"].head(1).tolist()[0].keys())] = df2["related"].apply(
                lambda x: pd.Series([x[key] for key in x.keys()]))

            related = df2.rename(columns={"index": "related_index",
                                           "videoId": "related_videoId",
                                           "source": "related_source",
                                           "title": "related_title"
                                           })

            related = related.drop('related', 1)
            related = pd.concat([related.drop(['likeInfo'], axis=1), related['likeInfo'].apply(pd.Series)], axis=1)
            related = pd.concat([related.drop(['viewInfo'], axis=1), related['viewInfo'].apply(pd.Series)], axis=1)
            save(related, path)

        if config['last'] == False and config['personal'] == '' and config['video'] == '' and config['related'] == '':
            print('No output type specified, please specify an argument among: --last, --personal, --video, --related.')

if __name__ == "__main__":
    main()