
import os
import sys
script_dir = os.path.dirname(os.path.dirname(__file__)) #<-- absolute dir the dir of the script is in
rel_path = "lib"
sys.path.append(os.path.join(script_dir, rel_path))
import API, tools, viz

# from lib import API, tools

id = 'af4b578f432046bb5569e024d48319419652bfc0';
df =  API.getDF(id, 'summary', 20000, 0)
df = tools.setDatetimeIndex(df, 'impression')
df = tools.setDatetimeIndexFloor(df, '1H')
df = tools.setTimeframe(df, '2019-03-19', '2019-04-03')
df = tools.doAggregation(df)
tools.saveHtml(df, 'impressions_count')
