from lib import API, tools
import configargparse
import os

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
            save(last, path)

        if config['personal'] != '':
            path = config['path'] + '/personal'
            personal = API.getPersonal(config['personal'])
            save(personal, path)

        if config['video'] != '':
            path = config['path'] + '/video'
            video = API.getVideo(config['video'])
            save(video, path)

        if config['related'] != '':
            path = config['path'] + '/related'
            related = API.getRelated(config['related'])
            save(related, path)

        if config['last'] == False and config['personal'] == '' and config['video'] == '' and config['related'] == '':
            print('No output type specified, please specifiy an argument among: --last, --personal, --video, --related.')

if __name__ == "__main__":
    main()