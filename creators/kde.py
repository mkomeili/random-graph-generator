import numpy as np
import pandas as pd
import plotnine as p9
import altair as alt
from utils.creators import unpack_graph_object
from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object, generate_indices_list

def create_bokeh_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y)    
    layer_names = convert_numbers_to_letters(range(num_layers))

    # create plot
    p = figure(
        toolbar_location=None,
        width = styles.get('width'),
        height = styles.get('height'),
    )
    for i in range(X.shape[0]):
        p.line(
            X[i],
            y[i], 
            line_color=styles.get('color')[i], 
            line_width=styles.get('line_thickness'), 
            alpha=0.7,
            legend_label=layer_names[i],
        )

    p.y_range.start = 0
    p.xaxis.axis_label = 'X'
    p.yaxis.axis_label = 'y'
    p.grid.grid_line_color="white"

    # render legend if applicable
    p.legend.title = styles.get('legend_title')
    p.legend.visible = styles.get('show_legend')

    return p

def create_altair_graph(graph_object):
     # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)

    # create labels to group layers by
    layer_names = convert_numbers_to_letters(generate_indices_list(y))

    # format data to be appropriate for a data frame
    X = X.flatten()
    y = y.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # render legend if applicable 
    legend = alt.Legend(title=styles.get('legend_title'), orient=styles.get('legend_position')) if styles.get('show_legend') else None

    # create line chart
    p = alt.Chart(df).mark_line().encode(
        x=alt.X('X', scale=alt.Scale(domain=[np.amin(X), np.amax(X)], nice=False)),
        y=alt.Y('y:Q'),
        color=alt.Color('layer_names:N', scale=alt.Scale(range=styles.get('color')), legend=legend),
        strokeWidth=alt.value(styles.get('line_thickness')),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )

    return p

def create_plotnine_graph(graph_object):
     # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    
    # format data to be appropriate for a data frame
    layer_names = convert_numbers_to_letters(generate_indices_list(y))
    X = X.flatten()
    y = y.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })
    
    # make plot for each layer
    p = (
        p9.ggplot(
            data=df, 
            mapping=p9.aes(
                x='X', 
                y='y',
                color=layer_names,
                fill=layer_names,
            )
        ) 
        + p9.geom_line(show_legend=styles.get('show_legend'), size=styles.get('line_thickness')) 
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')), legend_position=tuple(styles.get('legend_position')))
        + p9.scale_color_manual(values=styles.get('color'))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.labs(color=styles.get('legend_title'))
    )

    return p