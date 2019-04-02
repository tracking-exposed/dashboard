from lib import API, tools

id = ''
df =  API.getDF(id, 'summary', 20000, 0)
df = tools.setDatetimeIndex(df, 'impression')
df = tools.setDatetimeIndexFloor(df, '1H')
df = tools.setTimeframe(df, '2019-03-19', '2019-04-03')
df = tools.doAggregation(df)
tools.saveHtml(df, 'impressions_count')
