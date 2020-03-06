from datetime import date
from os.path import dirname, join
import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Panel, Select, CustomJS
from bokeh.models.widgets import TableColumn, DataTable, Button, TextInput, DateRangeSlider
import re

def explore_tab(df):

    def get_dataset(src, name, words, start, end):
        df = src[src.user == name].copy()
        mask = (df['timestamp'] > start) & (df['timestamp'] <= end)
        df = df[mask]
        words = [str(i) for i in words.split()]
        safe_words = []
        for word in words:
            word = re.escape(word)
            word = "(?=.*{})".format(word)
            safe_words.append(word)

        df = df[df['texts'].str.contains(''.join(safe_words))]

        source = ColumnDataSource(data=dict())

        cols = ['texts', 'displaySource', 'source']
        df[cols] = df[cols].replace({',': '', ',,': '', ';': ''}, regex=True)

        source.data = {
                    # 'index': df.index,
                    'impressionTime': df.impressionTime,
                    'impressionOrder': df.impressionOrder,
                    'source': df.source,
                    'fblinktype': df.fblinktype,
                    'texts': df.texts,
                    'textsize': df.textsize,
                    'publicationTime': df.publicationTime,
                    'permaLink': df.permaLink,
                    'nature': df.nature,
                    'ANGRY': df.ANGRY,
                    'HAHA': df.HAHA,
                    'LIKE': df.LIKE,
                    'LOVE': df.LOVE,
                    'SAD': df.SAD,
                    'WOW': df.WOW,
                    'displaySource': df.displaySource,
                    'id': df.id,
                    'timestamp': df.timestamp,
                    # 'images': df.images,
                    # 'opengraph': df.opengraph,
                    'postId': df.postId,
                    # 'semanticCount': df.semanticCount,
                    # 'semanticId': df.semanticId,
                    'sourceLink': df.sourceLink,
                    'timeline': df.timeline,
                    'user': df.user,
                    # 'videoautoplay': df.videoautoplay
            }
        return source

    def make_table(source):
        # Columns of tablem
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
                               columns=table_columns, width=1400)
        return user_table

    def update(attrname, old, new):
        name = name_select.value
        text_filter = text_input.value
        start = date_slider.value[0]
        end = date_slider.value[1]
        src = get_dataset(df, name, text_filter, start, end)
        source.data.update(src.data)

    name = df.user.iloc[0]
    words = ''
    names = df.user.unique()
    start = df.timestamp.min()
    end = df.timestamp.max()

    name_select = Select(value=name, title='User', options=sorted(names))
    text_input = TextInput(value="", title="Filter text:")
    date_slider = DateRangeSlider(title="Date Range: ", start=df.timestamp.min(), end=date.today(),
                                        value=(df.timestamp.min(), date.today()), step=1,
                                  callback_policy='mouseup')

    button = Button(label="Download", button_type="success")

    source = get_dataset(df, name, words, start, end)

    table = make_table(source)

    name_select.on_change('value', update)
    text_input.on_change('value', update)
    date_slider.on_change('value', update)

    button.js_on_click(CustomJS(args=dict(source=source),
                                code=open(join(dirname(__file__), "download.js")).read()))

    controls = column(name_select, date_slider, text_input, button)
    tab = Panel(child=row(table, controls), title='Explore')
    return tab
