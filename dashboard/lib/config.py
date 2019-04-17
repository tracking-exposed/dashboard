import configargparse, datetime
import os
abs_path = os.path.dirname(os.path.dirname(__file__))
rel_path = 'local/'
save_path = os.path.join(abs_path, rel_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
p.add('-n', '--name', help='name for your facebook profile', required=True)
p.add('-i', '--id', help='id of your fbtrex user', required=True)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-s', '--start', help='start date', default=str(datetime.date.today()-datetime.timedelta(days=7)))
p.add('-e', '--end', help='end date (non inclusive)', default=str(datetime.date.today()+datetime.timedelta(days=1)))
p.add('-p', '--path', help='path to save to (default dashboard-git/dashboard/local/', default=save_path)
p.add('--csv', dest='csv', action='store_true', default= False, help='create a csv')
p.add('--png', dest='png', action='store_true', default=False, help='create a png')
p.add('--html', dest='html', action='store_true', default=False, help='create a html')
p.add('--json', dest='json', action='store_true', default=False, help='create a json')
p.add('--impression-count', dest='impression-count', action='store_true', default=False, help='perform impression count instead of getting the whole data')
config = vars(p.parse_args())
