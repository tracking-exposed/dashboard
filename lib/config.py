import configargparse

# load configuration
p = configargparse.ArgParser(
    # default_config_files=[os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/general.conf"))]
)
p.add('-n', '--name', help='arbitrary name for profile', required=True)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-i', '--id', help='id of your fbtrex user', required=True)
config = vars(p.parse_args())
