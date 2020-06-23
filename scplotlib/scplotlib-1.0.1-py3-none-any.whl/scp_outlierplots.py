import numpy as np
import altair as alt


from .scp_core import BarPlot, LinePlot, ScatterPlot


def PlotOutlierScores(
    sc,
    outlier_score,
    color_by,
    threshold,
    width = 200,
    height = 200
):

    df = sc.celldata.loc[:, [color_by, outlier_score, threshold]]
    df = df.sort_values(by = [color_by])
    idx = np.arange(df.shape[0]) + 1 # Change so that first cell index is one
    df.insert(0, "Cells", idx, True)

    bar = BarPlot(
        df, 
        x = 'Cells:O', 
        y = outlier_score,
        color_by = color_by,
        bar_color = 'red',
        bar_size = 1
        )

    line = LinePlot(
        df, 
        x = 'Cells:O',
        y = threshold,
        color_by = None, 
        style_by = None, 
        size_by = None,
        line_color = 'black',
        line_style = [2, 4],
        line_size = 1
    )

    
    return (bar + line).configure_axis(grid = False).configure_view(strokeWidth = 0).properties(width = width, height = height)



