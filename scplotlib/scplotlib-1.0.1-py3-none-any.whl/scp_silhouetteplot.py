import numpy as np
import altair as alt


alt.data_transformers.disable_max_rows()

from sklearn.metrics import silhouette_samples

from .scp_themes import nature_theme
alt.themes.register("nature_theme", nature_theme)
alt.themes.enable("nature_theme")

# Compute Silhouette Score
def ComputeSilhouette(sc, cluster_by):

    cell_labels = sc.getNumericCellLabels(cluster_by)

    X = sc.getCounts() # X is (features, samples)

    sil_scores = silhouette_samples(X.T, cell_labels)

    sc.addCellData(col_data = sil_scores, col_name = 'Silhouette Index')

    return sc

    

def SilhouettePlot(sc, cluster_by):

    sc = ComputeSilhouette(sc, cluster_by)

    df = sc.celldata.loc[:, [cluster_by, 'Silhouette Index']]
    df = df.sort_values(by=[cluster_by, 'Silhouette Index'])
    idx = np.arange(df.shape[0]) + 1 # Change so that first cell index is one
    df.insert(0, "Cells", idx, True)

    chart = alt.Chart(df).mark_area().encode(
        x = alt.X('Silhouette Index', title='Silhouette Index'),
        y = alt.Y("Cells:O", axis=alt.Axis(labelOverlap=True, ticks=False)),
        color = alt.Color(cluster_by, type = 'ordinal', scale=alt.Scale(range = 'category'))
    ).properties(
        height = 250,
        width = 200
    )

    rule = alt.Chart(df).mark_rule(color='black').encode(
        x = alt.X('Silhouette Index', title = '', type = "quantitative", aggregate = "mean"),
        strokeDash = alt.value([2, 4])
    )

    return (chart + rule).configure_axis(grid=False).configure_view(strokeWidth=0)