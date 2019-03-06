import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

print('Welcome to the fbtrex dashboard configuration setup script.')
name = input('Please, select a name for this profile configuration:\n_ ')
print('\nThank you, this will be the name of your new configuration file: '+name)
rel_path = "config/"+name
file = os.path.join(script_dir, rel_path)
command = os.path.join(script_dir, 'test/tester.py')

with open(file, 'w+') as f:
    f.write('# see README.md for more infos\n')
    f.write('--name '+name+'\n')
    id = input('\nPlease paste the unique id for your user:\n_ ')
    f.write('--id '+id+'\n')
    print('\nDone! saving to \''+file+'\'')
    print('\n\nRemember you can call this specific configuration file by using:')
    print('python3 ' + command + ' -c ' + file)
