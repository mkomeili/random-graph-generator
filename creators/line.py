import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object, generate_indices_list

def create_bokeh_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y)    
    layer_names = convert_numbers_to_letters(range(num_layers))

    # create plot
    p = figure(
        width=styles.get('width'),
        height=styles.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    
    # draw each line individually
    for i, y_list in enumerate(y):
        p.line(X, y_list, color=styles.get('color')[i], line_width=styles.get('line_thickness'), legend_label=layer_names[i])
        getattr(p, styles.get('marker_type'))(X, y_list, color=styles.get('color')[i], size=styles.get('marker_size'))
    
    # render legend if applicable
    p.legend.title = styles.get('legend_title')
    p.legend.visible = styles.get('show_legend')
    
    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y)

    # format data to be appropriate for a data frame
    layer_names = convert_numbers_to_letters(generate_indices_list(y))
    X = np.append(X, [X] * (num_layers - 1))
    y = y.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # render legend if applicable 
    legend = alt.Legend(title=styles.get('legend_title'), orient=styles.get('legend_position')) if styles.get('show_legend') else None

    # base chart
    base = alt.Chart(df)

    # create points
    points = alt.LayerChart()
    if styles.get('marker_type') != None:
        marker = getattr(base, 'mark_{marker_type}'.format(marker_type=styles.get('marker_type')))
        points = marker(
            filled=True,
            size=alt.Value(styles.get('marker_size')),
        ).encode(
            x='X',
            y='y',
            color=alt.Color('layer_names:N', scale=alt.Scale(range=styles.get('color'))),
        )

    # create lines
    lines = base.mark_line().encode(
        x=alt.X('X', scale=alt.Scale(domain=[np.amin(X), np.amax(X)], nice=False)),
        y=alt.Y('y:Q'),
        color=alt.Color('layer_names:N', scale=alt.Scale(range=styles.get('color')), legend=legend),
        strokeWidth=alt.value(styles.get('line_thickness')),
    )

    # merge graphs
    p = alt.layer(
        lines,
        points
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )

    return p

def create_plotnine_graph(graph_object):
     # unpack data
    (X, y_layers, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)

    # format data to be appropriate for a data frame
    layer_names = convert_numbers_to_letters(generate_indices_list(y_layers))
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y_layers,
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
            ),
        ) 
        + p9.geom_line(show_legend=styles.get('show_legend'), size=styles.get('line_thickness'))
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')), legend_position=tuple(styles.get('legend_position')))
        + p9.scale_color_manual(values=styles.get('color'))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.labs(color=styles.get('legend_title'))
    )

    if styles.get('marker_type') != None:
        p += p9.geom_point(show_legend=False, size=styles.get('marker_size'), shape=styles.get('marker_type'))

    return p