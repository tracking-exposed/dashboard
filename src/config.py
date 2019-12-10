import configargparse
import os

'''
This module initializes the hierarchical configuration.
We want to be able to share config files between scripts,
so we create a parser "p" which we can import and then turn it
into actionable variables with "config = vars(p.parse_args())".
'''

dashboard_folder = os.path.dirname(os.path.dirname(__file__))
outputs_relative_path = 'outputs'
SAVE_PATH = os.path.join(dashboard_folder, '.', outputs_relative_path)

p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)

p.add('-n', '--name', help='Name for your facebook profile.')
p.add('-t', '--token', help='Personal token for your facebook.tracking.exposed extension.', required=True)
p.add('-c', '--config', is_config_file=True, help='Configuration file. Check configargparse documentation for formats.')
p.add('-p', '--path', help='Path to save to (default: "outputs").', default=SAVE_PATH)

# config = vars(p.parse_args())
