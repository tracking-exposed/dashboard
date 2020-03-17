import pandas as pd
import numpy as np
from math import pi
import sys
sys.path.append('..')
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Panel, Select, Div, Plot, Line,LinearAxis,Grid, DatetimeTickFormatter, Title
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

def diet_tab(df):
    df = df[['user', 'source', 'impressionOrder', 'impressionTime', 'nature']]
    df.index = pd.to_datetime(df.impressionTime).dt.floor('d')
    df['source'] = df['source'].astype(str)
    def cumulative_plot(daily_source):
        
        t = Title()
        t.text = 'Source Cumulative Count'
        plot = Plot(
            title=t, plot_width=1200, plot_height=300,
            min_border=0, toolbar_location=None)
        cumulative = Line(x="index", y="cumulative_count", line_color="#220000", line_width=3, line_alpha=0.6)

        plot.add_glyph(daily_source, cumulative)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def count_plot(daily_source):
        t = Title()
        t.text = 'Source_count'
        
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)
        source_count = Line(x="index", y="source_count", line_color="#93bf99", line_width=3, line_alpha=0.6)

        plot.add_glyph(daily_source, source_count)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def source_MA_7_plot(daily_source):
        
        t = Title()
        t.text = 'Source Count MA7'
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)

        mean_7 = Line(x="index", y="count_MA_7", line_color="#a2c4a7", line_width=3, line_alpha=0.6)
        plot.add_glyph(daily_source, mean_7)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def source_MA_30_plot(daily_source):
        
        t = Title()
        t.text = 'Source Count MA30'
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)

        mean_30 = Line(x="index", y="count_MA_30", line_color="#abd3b1", line_width=3, line_alpha=0.6)
        plot.add_glyph(daily_source, mean_30)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def order_plot(daily_source):
        t = Title()
        t.text = 'Order Mean'
        
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)
        source_count = Line(x="index", y="order_mean", line_color="#6d60c1", line_width=3, line_alpha=0.6)

        plot.add_glyph(daily_source, source_count)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def order_MA_7_plot(daily_source):
        
        t = Title()
        t.text = 'Order Mean MA7'
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)

        mean_7 = Line(x="index", y="order_MA_7", line_color="#9d97c6", line_width=3, line_alpha=0.6)
        plot.add_glyph(daily_source, mean_7)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def order_MA_30_plot(daily_source):
        
        t = Title()
        t.text = 'Order Mean MA30'
        plot = Plot(
            title=t, plot_width=400, plot_height=300,
            min_border=0, toolbar_location=None)

        mean_30 = Line(x="index", y="order_MA_30", line_color="#c4bdef", line_width=3, line_alpha=0.6)
        plot.add_glyph(daily_source, mean_30)
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
        plot.xaxis.major_label_orientation = pi / 4
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
        return plot

    def get_dataset(df,
                    user, source):
        df = df[(df['user'] == user) & (df['source'] == source)]
        daily_count = df.groupby(df.index).agg({'impressionOrder': 'mean', 'source': 'count'})
        daily_cumulative = df.groupby(['source']).cumcount(ascending=False).groupby(df.index).max()
        daily = pd.concat([daily_count, daily_cumulative], axis=1, sort=False)
        daily.columns = ['order_mean', 'source_count', 'cumulative_count']
        daily.cumulative_count = daily.cumulative_count + 1
        daily['order_MA_7'] = daily.order_mean.rolling(window=7).mean()
        daily['count_MA_7'] = daily.source_count.rolling(window=7).mean()
        daily['order_MA_30'] = daily.order_mean.rolling(window=30).mean()
        daily['count_MA_30'] = daily.source_count.rolling(window=30).mean()

        daily_source = ColumnDataSource(data=dict())
        daily_source.data = {
            'index': daily.index,
            'order_mean': daily.order_mean,
            'source_count': daily.source_count,
            'cumulative_count': daily.cumulative_count,
            'order_MA_7': daily.order_MA_7,
            'count_MA_7': daily.count_MA_7,
            'order_MA_30': daily.order_MA_30,
            'count_MA_30': daily.count_MA_30,
        }

        return daily_source

    def update(attrname, old, new):
        name = name_select.value
        source = source_select.value
        print("callback with "+name)
        daily_source_t = get_dataset(df,name,source)
        daily_source.data.update(daily_source_t.data)

    # init vars
    name = df.user.iloc[0]
    names = df.user.unique()
    sources = list(df.source.value_counts().nlargest(35).index)
    sources = [x for x in sources if str(x) != 'nan']
    print(sources[0])
    source = sources[0]

    # init controls
    name_select = Select(value=name, title='User', options=sorted(names))
    source_select = Select(value=str(source), title='Source', options=sources)

    # get data
    daily_source = get_dataset(df, name, source)

    # generate plots
    cumulative_plot = cumulative_plot(daily_source)
    count_plot = count_plot(daily_source)
    source_MA_7_plot = source_MA_7_plot(daily_source)
    source_MA_30_plot = source_MA_30_plot(daily_source)
    order_plot = order_plot(daily_source)
    order_MA_7_plot = order_MA_7_plot(daily_source)
    order_MA_30_plot = order_MA_30_plot(daily_source)

    # order_ graph = bar_order(posts_vs_ads_source)

    # callbacks
    name_select.on_change('value', update)
    source_select.on_change('value', update)

    # layout
    controls = row(name_select, source_select)
    tab = Panel(child=column(controls,cumulative_plot,column(row(count_plot,source_MA_7_plot,source_MA_30_plot,),
                             row(order_plot,order_MA_7_plot,order_MA_30_plot))
                                  ),
                title='Diet')
    return tab
