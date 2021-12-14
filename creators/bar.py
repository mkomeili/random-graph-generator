import pandas as pd
import altair as alt
import plotnine as p9

from utils.creators import unpack_graph_object
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, VBar, HBar

def create_bokeh_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    df = ColumnDataSource(dict(X=X, top=y))

    # create plot
    p = figure(
        title=None,
        width=styles.get('width'),
        height=styles.get('height'),
        min_border=0,
        toolbar_location=None,
        x_range=X if is_vertical else None,
        y_range=X[::-1] if not is_vertical else None,
    )

    # create glyphs based on vertical or horizontal
    glyph = (VBar(x='X', top='top', bottom=0, width=styles.get('bar_width')) if is_vertical
        else HBar(y='X', right='top', left=0, height=styles.get('bar_width')))
    p.add_glyph(df, glyph)

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
    })

    # horizontal forces x to take the y values as quantitive
    encodings = { 'x': 'x:O', 'y': 'y:Q' } if is_vertical else { 'x': 'y:Q', 'y': 'x:O' }
    
    chart = alt.Chart(df).mark_bar().encode(
        **encodings,
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )
    return chart

def create_plotnine_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create plot
    p = p9.ggplot(df, p9.aes(x='X', y='y')) + p9.geom_bar(stat='identity') 
    if not is_vertical: p += p9.coord_flip()

    return p