import sys, os
script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the dir of the script is in
rel_path = "trex-dash-lib"
sys.path.append(os.path.join(script_dir, rel_path))
import tools

#this while is used to keep cache alive until the problem is found with pickle
while True:
    cmd = input('Please say run or exit: _')
    if cmd == 'run':
        tools.saveDailyImpressions(tools.config)
    elif cmd == 'exit':
        exit()
    else:
        print('incorrect command, try again')
