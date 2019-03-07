import sys, os
script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the dir of the script is in
rel_path = "lib"
sys.path.append(os.path.join(script_dir, rel_path))
import API, tools, viz
from config import config


#this while is used to keep cache alive until the problem is found with pickle
while True:
    cmd = input('Please say run or exit: _')
    if cmd == 'run':
        df = API.getSummary(config['id'])  # first we call an API
        list = tools.doTimelineList(df)  # we want to retrieve a list of timeline ids from the dataframe to filter it
        df = tools.doImpressionCount(df, list)  # produces a dataframe with timeline startdates and impression count
        df = tools.setTimeframe(df, start='2019-03-06', end='2019-03-06')  # returns a filtered datetime index at start of (today - days). days are days to go behind
        chart = viz.impressionCount(df)  # produces a chart
        chart = viz.formatDates(chart) # makes chart pretty(ier)
        viz.savePng(chart, 'antonio_1')
    elif cmd == 'exit':
        exit()
    else:
        print('incorrect command, try again')
