import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from bokeh.models import ColumnDataSource, Panel
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Panel, Select, Div
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models.widgets import TableColumn, DataTable, Slider  #, Button, TextInput, DateRangeSlider

from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap



def stats_tab(posts_vs_ads, scrolling_time, source_count, post_count):
    def timespent_div(scrolling_time):
        print('creating new timespent_div')
        div = Div(text="""User """ + str(list(scrolling_time.data["user"]))[2:-2] + """ spent a total of <b>""" + str(list(scrolling_time.data["time_spent"]))[2:-2] + """</b> scrolling facebook in the browser where
        facebook.tracking.exposed was installed.""",
                  width=200, height=200)
        return div

    def post_ads_bar(posts_vs_ads):
        print("Making new bar plot for post_ads")
        p = figure(x_range=posts_vs_ads.data["type"], plot_height=350, toolbar_location=None, title="Posts vs Ads Counts")
        p.vbar(x='type', top='count', width=0.9, source=posts_vs_ads, legend_field="type",
               line_color='white', fill_color=factor_cmap('type', palette=Spectral6, factors=posts_vs_ads.data["type"]))

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = max(posts_vs_ads.data["count"])+(max(posts_vs_ads.data["count"])/100)*25
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        return p

    def top_sources_table(source_count):
        # Columns of table
        table_columns = [TableColumn(field='source', title='Source'),
                         TableColumn(field='count', title='Count'),
                         TableColumn(field='nature', title='Nature')
                         ]

        table = DataTable(source=source_count,
                               columns=table_columns, width=400, height=200)
        return table

    def top_posts_table(post_count):

        table_columns = [TableColumn(field='source', title='Source'),
                         TableColumn(field='texts', title='Title'),
                         TableColumn(field='count', title='Count'),
                         TableColumn(field='link', title='URL')
                         ]

        table = DataTable(source=post_count,
                          columns=table_columns, width=400, height=200)
        return table

    def get_dataset(posts_vs_ads,
                    scrolling_time,
                    source_count,
                    post_count,
                    user, ntop):
        scrolling_time.columns = ['user', 'time_spent']
        posts_vs_ads_temp = posts_vs_ads[posts_vs_ads['user'] == user]
        posts_vs_ads_temp = posts_vs_ads_temp.set_index('user')[['organic', 'sponsored']].T.reset_index()
        posts_vs_ads_temp.columns = ['type', 'count']
        scrolling_time_temp = scrolling_time[scrolling_time['user'] == user]
        source_count_temp = source_count[(source_count['user'] == user)].nlargest(int(ntop), 'count')
        post_count_temp = post_count[(post_count['user'] == user)].nlargest(int(ntop), 'count')
        posts_vs_ads_source = ColumnDataSource(data=dict())
        posts_vs_ads_source.data = {
            'type': posts_vs_ads_temp.type,
            'count': posts_vs_ads_temp['count']
        }
        scrolling_time_source = ColumnDataSource(data=dict())
        scrolling_time_source.data = {
            'user': scrolling_time_temp.user,
            'time_spent': scrolling_time_temp.time_spent}
        print(scrolling_time_source.data)

        source_count_source = ColumnDataSource(data=dict())
        source_count_source.data = {
            'user': source_count_temp.user,
            'nature': source_count_temp.nature,
            'source': source_count_temp.source,
            'count': source_count_temp['count']
        }
        post_count_source = ColumnDataSource(data=dict())
        post_count_source.data = {
            'user': post_count_temp.user,
            'source': post_count_temp.source,
            'texts': post_count_temp.texts,
            'link': post_count_temp.permaLink,
            'count': post_count_temp['count']
        }
        return posts_vs_ads_source,\
               scrolling_time_source,\
               source_count_source,\
               post_count_source

    def update(attrname, old, new):
        name = name_select.value
        ntop = top_select.value
        print("callback with "+name)
        posts_vs_ads_source_t, scrolling_time_source_t, source_count_source_t, post_count_source_t = get_dataset(posts_vs_ads,
                                                                                                         scrolling_time,
                                                                                                         source_count,
                                                                                                         post_count,
                                                                                                         name,
                                                                                                         ntop)
        posts_vs_ads_source.data.update(posts_vs_ads_source_t.data)
        scrolling_time_source.data.update(scrolling_time_source_t.data)
        timespent.text = """User """ + str(list(scrolling_time_source.data["user"]))[2:-2] + """ spent an estimate of <b>""" + str(list(scrolling_time_source.data["time_spent"]))[2:-12] + """</b> scrolling facebook in the browser where
        facebook.tracking.exposed was installed."""
        source_count_source.data.update(source_count_source_t.data)
        post_count_source.data.update(post_count_source_t.data)


    # init vars
    name = source_count.user.iloc[0]
    ntop = 3.0
    names = source_count.user.unique()
    source_table_title = Div(text="""Top Sources""", width=100, height=20)
    posts_table_title = Div(text="""Top Posts""", width=100, height=20)

    # init controls
    name_select = Select(value=name, title='User', options=sorted(names))
    top_select = Slider(title="# of top sources/posts", value=3.0, start=3.0, end=20.0, step=1.0)

    # get data
    posts_vs_ads_source, scrolling_time_source, source_count_source, post_count_source = get_dataset(posts_vs_ads,
                                                                                                     scrolling_time,
                                                                                                     source_count,
                                                                                                     post_count,
                                                                                                     name,
                                                                                                     ntop)


    # generate plots
    timespent = timespent_div(scrolling_time_source)
    postadspie = post_ads_bar(posts_vs_ads_source)
    topposts = top_posts_table(post_count_source)
    topsources = top_sources_table(source_count_source)

    # callbacks
    name_select.on_change('value', update)
    top_select.on_change('value', update)

    # layout
    controls = row(name_select, top_select)
    tab = Panel(child=column(controls,
                             row(timespent,
                                 postadspie),
                             row(column(posts_table_title, topposts),
                             column(source_table_title, topsources))
                                  ),
                title='Statistics')
    return tab
