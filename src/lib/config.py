import configargparse
import datetime
import os
abs_path = os.path.dirname(os.path.dirname(__file__))
rel_path = 'outputs'
save_path = os.path.join(abs_path, '..', rel_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
p.add('-n', '--name', help='name for your facebook profile')
p.add('-t', '--token', help='token of your fbtrex user', required=True)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-s', '--start', help='start date for harmonizer. default is a week ago', default=str(datetime.date.today()-datetime.timedelta(days=7)))
p.add('-e', '--end', help='end date for harmonizer. default is today.', default=str(datetime.date.today()))
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
p.add('--json', dest='json', action='store_true', default=False, help='create a json')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--granularity', help='floor for the datetimeindex (1H default, 1D for daily)', default='1H')
p.add('--sources', help='directory containing ONLY csv files from FBcrawl, used to merge with user data')
p.add('-s1', '--source1', help='string of the exact displayname for the first source')
p.add('-s2', '--source2', help='string of the exact displayname for the second source')
config = vars(p.parse_args())

'''argparse libreria python standard'''