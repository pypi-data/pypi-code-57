import altair as alt


import pandas as pd

from .scp_themes import nature_theme
alt.themes.register("nature_theme", nature_theme)
alt.themes.enable("nature_theme")

# Scatter Plot

def ScatterPlot(    dataframe, 
                    x,
                    y,
                    color_by, 
                    marker_by, 
                    size_by,
                    marker_color,
                    marker_shape,
                    marker_size, 
                    marker_thickness,
                    xlabel = None,
                    ylabel = None
                ):

    if (type(color_by) == type(None)):
        color = alt.value(marker_color)
    else:
        color = alt.Color(color_by, type = 'ordinal', scale=alt.Scale(range = 'category'))    

    if (type(marker_by) == type(None)):
        marker = alt.value(marker_shape)
    else:
        marker = alt.Shape(marker_by, type = 'ordinal')

    if (type(size_by) == type(None)):
        size = alt.value(marker_size)
    else:
        size = alt.Size(size_by, type = 'quantitative')
    
    if (type(xlabel) == type(None)):
        xlabel = x

    if (type(ylabel) == type(None)):
        ylabel = y


    chart = alt.Chart(dataframe).mark_point().encode(
        x = alt.X(x, title=xlabel),
        y = alt.Y(y, title=ylabel),
        shape = marker,
        color = color,
        size = size,
        strokeWidth = alt.value(marker_thickness)
    )

    return chart



# Bar Plot

def BarPlot(    
    dataframe,
    x, 
    y, 
    color_by,
    bar_color,
    bar_size,
    xlabel = None,
    ylabel = None
):

    if (type(color_by) == type(None)):
        color = alt.value(bar_color)
    else:
        color = alt.Color(color_by, type = 'ordinal', scale=alt.Scale(range = 'category'))

    if (type(xlabel) == type(None)):
        xlabel = x

    if (type(ylabel) == type(None)):
        ylabel = y

    chart = alt.Chart(dataframe).mark_bar().encode(
        #x = alt.X(x, title=xlabel, type='ordinal', axis=alt.Axis(labelOverlap=True, ticks=False)),
        x = alt.X(x, title=xlabel, axis=alt.Axis(ticks=False)),
        y = alt.Y(y, title=ylabel, type = 'quantitative'),
        color = color,
        size = alt.value(bar_size)
    )

    return chart



# Line Plot

def LinePlot(
    dataframe, 
    x,
    y,
    color_by, 
    style_by, 
    size_by,
    line_color,
    line_style,
    line_size,
    xlabel = None,
    ylabel = None
):

    if (type(color_by) == type(None)):
        color = alt.value(line_color)
    else:
        color = alt.Color(color_by, type = 'ordinal', scale=alt.Scale(range = 'category'))    

    if (type(style_by) == type(None)):
        style = alt.value(line_style)
    else:
        style = style_by

    if (type(size_by) == type(None)):
        size = alt.value(line_size)
    else:
        size = alt.Size(size_by, type = 'quantitative')

    if (type(xlabel) == type(None)):
        xlabel = x

    if (type(ylabel) == type(None)):
        ylabel = y

    chart = alt.Chart(dataframe).mark_line().encode(
        x = alt.X(x, title=xlabel),
        y = alt.Y(y, title=ylabel),
        color = color,
        size = size,
        strokeDash = style
    )

    return chart