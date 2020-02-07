import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.table import table_tab

# Read data into dataframes
data = pd.read_csv(join(dirname(__file__), '../outputs/fb', 'etc.csv'),
	                                          index_col=0).dropna()

# Formatted Flight Delay Data for map
other_data = pd.read_csv(join(dirname(__file__), 'data', 'etcetc.csv'),
                            header=[0,1], index_col=0)

# Create each of the tabs
tab1 = histogram_tab(data)
tab2 = density_tab(data)
tab3 = table_tab(data)
tab4 = map_tab(other_data)
tab5 = route_tb(data)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)