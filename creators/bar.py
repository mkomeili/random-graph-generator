from creators.utils import unpack_graph_object
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, VBar, HBar
import altair as alt
import pandas as pd

parameters = {
    'width': 300,
    'height': 300,
    'bar_width': 0.5,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, is_vertical), style = unpack_graph_object(graph_object)
    source = ColumnDataSource(dict(X=X, top=y))

    # create plot
    p = Plot(
        title=None,
        width=parameters['width'],
        height=parameters['height'],
        min_border=0,
        toolbar_location=None
    )

    # create glyphs based on vertical or horizontal
    glyph = (VBar(x="X", top="top", bottom=0, width=parameters['bar_width']) if is_vertical
        else HBar(y="X", right="top", left=0, height=parameters['bar_width']))
    p.add_glyph(source, glyph)

    # adjust axes
    xaxis, yaxis = LinearAxis(), LinearAxis()
    p.add_layout(xaxis, 'below')
    p.add_layout(yaxis, 'left')

    # cosmetic adjustments (makes graph look more elegant)
    p.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    p.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, is_vertical), style = unpack_graph_object(graph_object)
    source = pd.DataFrame({
        'x': X,
        'y': y,
    })

    # create plot
    if (is_vertical):
        chart = alt.Chart(source).mark_bar().encode(
            x = 'x:O',
            y = 'y:Q',
        ).properties(
            width=parameters['width'],
            height=parameters['height'],
        )
    else:
        # horizontal forces x to take the y values as quantitive
        chart = alt.Chart(source).mark_bar().encode(
            x = 'y:Q',
            y = 'x:O',
        ).properties(
            width=parameters['width'],
            height=parameters['height'],
        )  
    
    return chart

def create_plotnine_graph(graph_object):
    return {}