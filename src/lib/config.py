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
p.add('-p', '--path', help='path to save to (default "outputs")', default=save_path)

# config = vars(p.parse_args())