from lib import API, tools, viz
from lib.config import config

savename = config['name']+'_impressions_'+config['start'][2:]+'_'+config['end'][2:]

df =  API.getDf(config['id'], 'summary', 20000, 0)
df = tools.setDatetimeIndex(df, 'impression')
df = tools.setDatetimeIndexFloor(df, '1H')
df = tools.setTimeframe(df, config['start'], config['end'])
df = tools.countImpressions(df)

if config['csv'] == True:
    print('Saving CSV...')
    df.to_csv(config['path']+savename+'.csv')
    print('Saved to '+config['path']+savename+'.csv')

if config['html'] == True:
    print('Saving HTML...')
    tools.saveHtml(df, savename)

if config['png'] == True:
    print('Creating png...')
    viz.savePng(viz.formatDates(viz.impressionCount(df)), savename)
