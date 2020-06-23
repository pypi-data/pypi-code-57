import numpy as np
import pandas as pd
import altair as alt


from .scp_themes import nature_theme
alt.themes.register("nature_theme", nature_theme)
alt.themes.enable("nature_theme")
alt.data_transformers.disable_max_rows()


def GeneExpHeatmap(sc, color_by, sort_by, name_by, top_num_genes = 10, sort = 'descending'):
    
    cell_idx = np.arange(sc.dim[1]) + 1 # Cell indexes, first cell index is 1. 

    X = sc.getCounts() # X is (features, samples)
    legend_title = "Expression"

    labels = sc.getCellData(color_by) # Cell labels of the cells, can be numeric array or string array
    gene_names = sc.getGeneData(name_by)

    idx = np.argsort(labels)
    labels = labels[idx]
    X = X[:, idx]

    # Get the different cell types 
    cell_types = sc.getDistinctCellTypes(color_by)
    if (cell_types.dtype == np.float64): # if numeric and float, convert to integer
        cell_types = cell_types.astype(int)


    # Sort according to the gene score
    if (type(sort_by) != type(None)):
        sort_values = sc.getGeneData(sort_by)
        idx = np.argsort(sort_values)
        if (sort == 'descending'):
            idx = np.flip(idx)

        X = X[idx, :]
        gene_names = gene_names[idx]

    gene_names = gene_names[0:top_num_genes]
    X = X[0:top_num_genes, :]

    # Create dataframe for altair to do plotting
    C, G = np.meshgrid(cell_idx, gene_names)
    L, _ = np.meshgrid(labels, gene_names)
    source = pd.DataFrame({ 'Cells': C.ravel(),
                            'Genes': G.ravel(),
                            'Expression': X.ravel(),
                            'y': np.ones(C.ravel().shape[0]),
                            'labels': L.ravel()})


    # Draw the heatmap
    # 
    heatmap = alt.Chart(source).mark_rect().encode(
        x=alt.X('Cells:O', axis=alt.Axis(labelOverlap=True, ticks=False)),
        y=alt.Y('Genes'),
        color=alt.Color('Expression:Q', legend=alt.Legend(orient="right", title=legend_title), scale=alt.Scale(reverse = True, scheme="redyellowblue"))
    )

    # Draw lines using different colors for different cell types
    line = alt.Chart(source).mark_line(size = 8).encode(
        x=alt.X('Cells:O', axis = None),
        y=alt.Y('y', axis = None),
        color=alt.Color('labels:O', legend=alt.Legend(orient = 'top', direction = 'horizontal', title = color_by), scale=alt.Scale(range = 'category'))
    )

    return (heatmap + line).properties(height = 250, width = 200).configure_axis(grid=False).configure_view(strokeWidth=0)