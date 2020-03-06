# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def cleaning_tab(df):

	# Calculate summary stats for table

	stats = pd.DataFrame(columns=['user','start', 'end',
								  'average_impression_count',
								  'timelines',
								  'total_entries',
								  'missing values'
								  ])

	def getStats(df):
		user_list = df.user.unique()
		for user in user_list:
			data = df[(df['user'] == user)]

			stats.loc[user] = [
				user,
				data.impressionTime.min(),
				data.impressionTime.max(),
				# max(df.impressionOrder),
				# min(df.groupby(['timeline'], sort=False)['impressionOrder'].max()),
				data.impressionOrder.mean(),
				data['timeline'].nunique(),
				data['id'].count(),
				data.isna().sum().sum()
			]
		return stats

	stats = getStats(df)
	user_src = ColumnDataSource(stats)

	# Columns of table
	table_columns = [TableColumn(field='user', title='Username'),
					 TableColumn(field='start', title='Start'),
					 TableColumn(field='end', title='End'),
					 TableColumn(field='average_impression_count', title='Avg Impressions per Timeline'),
					 TableColumn(field='timelines', title='# of Timelines'),
					 TableColumn(field='total_entries', title='Total Entries'),
					 TableColumn(field='missing values', title='Missing Values')
					]

	user_table = DataTable(source=user_src,
							  columns=table_columns, width=1000)

	tab = Panel(child=user_table, title='Cleaning')

	return tab