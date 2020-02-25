import datetime
from os.path import dirname, join
import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable
from bokeh.models.widgets import TextInput
import re

def explore_tab(df):
    def get_dataset(src, name, filter):
        df = src[src.user == name].copy()
        filter = [str(i) for i in filter.split()]
        safe_filter = [re.escape(m) for m in filter]
        df = df[df['texts'].str.contains('&'.join(safe_filter))]
        return ColumnDataSource(data=df)

    def make_table(source):
        # Columns of table
        table_columns = [
            TableColumn(field='impressionTime', title='Time'),
            TableColumn(field='impressionOrder', title='Order'),
            TableColumn(field='source', title='Source'),
            TableColumn(field='fblinktype', title='Type'),
            TableColumn(field='texts', title='Text'),
            TableColumn(field='textsize', title='Text Size'),
            TableColumn(field='publicationTime', title='Publication Time'),
            TableColumn(field='permaLink', title='Link'),
            TableColumn(field='nature', title='Nature'),
            TableColumn(field='ANGRY', title='Angry'),
            TableColumn(field='HAHA', title='Haha'),
            TableColumn(field='LIKE', title='Like'),
            TableColumn(field='LOVE', title='Love'),
            TableColumn(field='SAD', title='Sad'),
            TableColumn(field='WOW', title='Wow')
        ]

        user_table = DataTable(source=source,
                               columns=table_columns, width=1000)
        return user_table

    def update_plot(attrname, old, new):
        name = name_select.value
        text_filter = text_input.value
        src = get_dataset(df, name, text_filter)
        source.data.update(src.data)

    name = df.user.iloc[0]
    filter = ''
    names = df.user.unique()

    name_select = Select(value=name, title='User', options=sorted(names))
    text_input = TextInput(value="", title="Filter text:")

    source = get_dataset(df, name, filter)
    table = make_table(source)

    name_select.on_change('value', update_plot)
    text_input.on_change('value', update_plot)

    controls = column(name_select, text_input)
    tab = Panel(child=row(table, controls), title='Explore')
    return tab