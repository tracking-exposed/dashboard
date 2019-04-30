import configargparse
# import datetime
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
# p.add('-s', '--start', help='start date. default is a week ago', default=str(datetime.date.today()-datetime.timedelta(days=7)))
# p.add('-e', '--end', help='end date (non inclusive). default is today.', default=str(datetime.date.today()+datetime.timedelta(days=1)))
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
p.add('--json', dest='json', action='store_true', default=False, help='create a json')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
summary = vars(p.parse_args())

ps = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
ps.add('-n', '--name', help='name for your facebook profile')
ps.add('-t', '--token', help='token of your fbtrex user', required=True)
ps.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)
ps.add('-c', '--config', is_config_file=True, help='config file path')
ps.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
ps.add('--json', dest='json', action='store_true', default=False, help='create a json')
ps.add('-a', '--amount', help='amount of entries to fetch from api', default=12)
ps.add('--skip', help='amount of entries to skip', default=0)
ps.add('--granularity', help='floor for the datetimeindex (1H default, 1D for daily)', default='1H')

status = vars(ps.parse_args())