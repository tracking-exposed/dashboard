import sys, os
script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the dir of the script is in
rel_path = "lib"
sys.path.append(os.path.join(script_dir, rel_path))
import API, tools, viz
from config import config

# this while is used to keep cache alive until the problem is found with pickle
while True:
    cmd = input('Type png to save png, html to save html, exit to exit: \n_')
    if cmd == 'png':
        df = API.getSummary(config['id'])  # first we call an API
        list = tools.doTimelineList(df)  # we want to retrieve a list of timeline ids from the dataframe to filter it
        df = tools.doImpressionCount(df, list)  # produces a dataframe with timeline startdates and impression count
        while True:
            try:
                timefr = input('Choose a start date (format yyyy-mm-dd OR yyyy-mm-dd HH:MM):\n_')
                data = tools.setTimeframe(df,
                                    start=timefr)  # returns a filtered datetime index at start of (today - days). days are days to go behind
                break
            except ValueError:
                print('invalid date, try again.')
                continue
        chart = viz.impressionCount(data)  # produces a chart
        chart = viz.formatDates(chart) # makes chart pretty(ier)
        viz.savePng(chart, config['name'])
        print('Saved: '+config['name'])

    elif cmd == 'html':
        df = API.getSummary(config['id'])  # first we call an API
        list = tools.doTimelineList(df)  # we want to retrieve a list of timeline ids from the dataframe to filter it
        df = tools.doImpressionCount(df, list)  # produces a dataframe with timeline startdates and impression count
        while True:
            try:
                timefr = input('Choose a start date (format yyyy-mm-dd OR yyyy-mm-dd HH:MM):\n_')
                data = tools.setTimeframe(df,
                                    start=timefr)  # returns a filtered datetime index at start of (today - days). days are days to go behind
                break
            except ValueError:
                print('invalid date, try again.')
                continue
        tools.saveHtml(data)
    elif cmd == 'exit':
        exit()
    else:
        print('incorrect command, try again')
