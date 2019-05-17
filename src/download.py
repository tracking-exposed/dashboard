from lib import API, tools
from lib.config import p
import datetime

p.add('-s', '--start', help='start date for harmonizer. default is a week ago', default=str(datetime.date.today()-datetime.timedelta(days=7)))
p.add('-e', '--end', help='end date for harmonizer. default is today.', default=str(datetime.date.today()))
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
p.add('--json', dest='json', action='store_true', default=False, help='create a json')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--api-source', help='Choose among: summary, status, ')
config = vars(p.parse_args())

'''

i want to download my data, this script should allow a user to get all the relevant data he wants.
--api summary,status,etc
--amount
--skip
--savepath
-- format csv or json

'''

def main(what='summary'):

        if config['name'] != None:
            path = config['path'] + '/' + config['name'] + '_summary'
        else:
            path = config['path'] + '/' + config['token'] + '_summary'

        df = API.getDf(config['token'], what, config['amount'], config['skip'])

        if config['csv']:
            print('Saving CSV to '+path+ '.csv')
            df.to_csv(tools.uniquePath(path + '.csv'), index=False)
        if config['json']:
            print('Saving JSON to '+path + '.json')
            df.to_json(tools.uniquePath(path + '.json'))

if __name__ == "__main__":
    main()