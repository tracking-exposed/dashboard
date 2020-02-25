import pandas as pd
from os.path import dirname, join
import os
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.table import table_tab
from scripts.explore import explore_tab

def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if str(f)[0] == '.':
                pass
            else:
                yield os.path.abspath(os.path.join(dirpath, f))


folder = "outputs/fb/summary/"
files = absoluteFilePaths(folder)


users = []
data = {}
for f in files:
    df = pd.read_csv(f)
    user = df.user.iloc[0].replace(" ","").lower()
    data.update({user: df})


df = pd.concat(data.values())




# Read data into dataframes (all of them)
# data = pd.read_csv(join(dirname(__file__),
#                         '../outputs/fb/summary/', '7b237b7e757467ad44d3ea3389f1b8ce53d95b48.csv'),
#                    index_col=0,
#                    nrows=10000
#                    )

# Create each of the tabs
tab1 = table_tab(df)
tab2 = explore_tab(df)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
