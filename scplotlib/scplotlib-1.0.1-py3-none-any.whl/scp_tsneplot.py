import altair as alt


from sklearn.manifold import TSNE
from .scp_core import ScatterPlot


from .scp_themes import nature_theme
alt.themes.register("nature_theme", nature_theme)
alt.themes.enable("nature_theme")

def ComputeTSNE(    sc, 
                    tsne_dist_metric,
                    tsne_init,
                    tsne_perplexity,
                    tsne_iterations,
                    tsne_learning_rate,
                    tsne_early_exaggeration,
                    tsne_random_state):

    tsne = TSNE(    n_components = 2, 
                    metric=tsne_dist_metric,
                    init= tsne_init,
                    perplexity=tsne_perplexity,
                    n_iter=tsne_iterations,
                    learning_rate=tsne_learning_rate,
                    early_exaggeration=tsne_early_exaggeration,
                    random_state=tsne_random_state
                    )

    X = sc.getCounts() # X is (features, samples)

    X_red = tsne.fit_transform(X.T)
    x = X_red[:, 0]
    y = X_red[:, 1]

    sc.addCellData(col_data = x, col_name = 't-SNE 1')
    sc.addCellData(col_data = y, col_name = 't-SNE 2')

    return sc



# Produces a t-SNE scatter plot
def tSNEPlot(   sc, 
                color_by = None, 
                marker_by = None, 
                size_by = None,
                marker_color = '#E64B35FF',
                marker_shape = 'circle',
                marker_size = 2, 
                marker_thickness = 1, 
                tsne_dist_metric = 'euclidean',
                tsne_init = 'random',
                tsne_perplexity = 30,
                tsne_iterations = 1000,
                tsne_learning_rate = 200,
                tsne_early_exaggeration = 12,
                tsne_random_state = None
                ):


    sc = ComputeTSNE(   sc, 
                        tsne_dist_metric,
                        tsne_init,
                        tsne_perplexity,
                        tsne_iterations,
                        tsne_learning_rate,
                        tsne_early_exaggeration,
                        tsne_random_state)

    chart = ScatterPlot(    sc.celldata,
                            x = 't-SNE 1',
                            y = 't-SNE 2',
                            color_by = color_by,
                            marker_by = marker_by,
                            size_by = size_by,
                            marker_color = marker_color,
                            marker_shape = marker_shape,
                            marker_size = marker_size,
                            marker_thickness = marker_thickness
                            )
                            
    return chart.configure_axis(grid = False).configure_view(strokeWidth = 0)