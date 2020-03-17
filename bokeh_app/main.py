import pandas as pd
import os
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from scripts.cleaning import cleaning_tab
from scripts.explore import explore_tab
from scripts.stats import stats_tab
from scripts.diet import diet_tab
from datetime import datetime
now = datetime.now()

def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if str(f)[0] == '.':
                pass
            else:
                yield os.path.abspath(os.path.join(dirpath, f))

folder = "outputs/fb/summary/"
aggregated_folder = "outputs/fb/aggregated/"
files = absoluteFilePaths(folder)

users = []
data = {}
for f in files:
    df = pd.read_csv(f)
    user = df.user.iloc[0].replace(" ","").lower()
    data.update({user: df})

df = pd.concat(data.values())
df['timestamp'] = pd.to_datetime(df['impressionTime']).astype(int)/1000000
posts_vs_ads = pd.read_csv(aggregated_folder+'posts_vs_ads.csv')
scrolling_time = pd.read_csv(aggregated_folder+'scrolling_time.csv')
source_count = pd.read_csv(aggregated_folder+'source_count.csv')
post_count = pd.read_csv(aggregated_folder+'post_count.csv')


# Create each of the tabs
tab1 = cleaning_tab(df)
tab2 = explore_tab(df)
tab3 = stats_tab(posts_vs_ads,scrolling_time,source_count,post_count)
tab4 = diet_tab(df)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

print('Elapsed time: {}'.format(str(datetime.now()-now)))
