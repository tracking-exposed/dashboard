from lib import API, tools, viz
from lib.config import config

if config['impression-count'] == True:
    savename = config['name'] + '_impressions_' + config['start'] + '_' + config['end']
    df =  API.getDf(config['id'], 'summary', 30000, 0)
    df = tools.setDatetimeIndex(df, 'impression')
    df = tools.setDatetimeIndexFloor(df, '1H')
    df = tools.setTimeframe(df, config['start'], config['end'])
    df = tools.countImpressions(df)
    if config['csv'] == True:
        print('Saving CSV...')
        df.to_csv(config['path']+savename+'.csv', index=True)
        print('Saved to '+config['path']+savename+'.csv')
    if config['json'] == True:
        print('Saving JSON...')
        df.to_json(config['path'] + savename + '.json')
        print('Saved to ' + config['path'] + savename + '.json')
    if config['html'] == True:
        print('Saving HTML...')
        tools.saveHtml(df, savename)
    if config['png'] == True:
        print('Saving PNG...')
        viz.savePng(viz.formatDates(viz.impressionCount(df)), savename)
else:
    df =  API.getDf(config['id'], 'summary', 30000, 0)
    savename = config['name'] + '_' + config['start'] + '_' + config['end']
    if config['csv'] == True:
        print('Saving CSV...')
        df.to_csv(config['path'] + savename + '.csv', index=False)
        print('Saved to ' + config['path'] + savename + '.csv')

    if config['json'] == True:
        print('Saving JSON...')
        df.to_json(config['path'] + savename + '.json')
        print('Saved to ' + config['path'] + savename + '.json')

    if config['html'] == True:
        print('Saving HTML...')
        tools.saveHtml(df, savename)

    if config['png'] == True:
        print('Cant save a PNG for the whole data yet, use --impression-count')
