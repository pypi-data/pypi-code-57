
import altair as alt


from sklearn.decomposition import PCA
from .scp_core import ScatterPlot


from .scp_themes import nature_theme
alt.themes.register("nature_theme", nature_theme)
alt.themes.enable("nature_theme")

def ComputePCA(sc):

    X = sc.getCounts()
    pca = PCA(n_components=2)
    X_red = pca.fit_transform(X.T)
    x = X_red[:, 0]
    y = X_red[:, 1]

    sc.addCellData(col_data = x, col_name = 'PC1')
    sc.addCellData(col_data = y, col_name = 'PC2')

    return sc

def PCAPlot(    sc, 
                color_by = None, 
                marker_by = None, 
                size_by = None,
                marker_color = '#E64B35FF',
                marker_shape = 'circle',
                marker_size = 2, 
                marker_thickness = 1
                ):

    sc = ComputePCA(sc)
    
    chart = ScatterPlot(    sc.celldata,
                            x = 'PC1',
                            y = 'PC2',
                            color_by = color_by,
                            marker_by = marker_by,
                            size_by = size_by,
                            marker_color = marker_color,
                            marker_shape = marker_shape,
                            marker_size = marker_size,
                            marker_thickness = marker_thickness
                            )

    return chart.configure_axis(grid = False).configure_view(strokeWidth = 0)