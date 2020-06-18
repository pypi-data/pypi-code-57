import plotly.graph_objects as go


def getShapeMatrix(ro=1.3, N=1000, gpu=False):
    if gpu:
        import cupy as np
    else:
        import numpy as np

    def f(ro, N):
        ''' give the surface map matrix '''
        # polar coordinate
        theta = np.linspace(0, 2 * np.pi, N)
        x = ro * np.cos(theta)
        y = ro * np.sin(theta)

        u, v = np.meshgrid(x, y)
        RO = u**2 + v**2
        # map z to u,v
        Z = 1 - u / RO - RO
        return x, y, Z

    x, y, Z = f(ro, N)
    # remap z to the grid index
    index_x, index_y = np.argsort(x), np.argsort(y)
    Y, X = np.meshgrid(
        index_x,
        index_y)  # meshgrid always will use numpy array NOT mxnet NDArray
    Z = Z[X, Y]
    return Z


def love():
    res = getShapeMatrix(ro=1.3, N=150, gpu=False)[12:129, :100]
    # res[res<-0.9] = 0
    res[res > 5] = 0
    res = 1 - res
    res[res > 1] = 1
    res[res < -3] = -3
    res = res + 3
    res /= 4

    fig = go.Figure(data=[
        go.Surface(
            z=res,
            # colorscale='Viridis',
            showscale=False,
            opacity=0.9)
    ])
    fig.update_layout(
        title='noise distribution',
        autosize=False,
        width=700,
        height=700,
    )
    fig.update_traces(contours_z=dict(show=True,
                                      usecolormap=True,
                                      highlightcolor="limegreen",
                                      project_z=True))
    fig.show()


if __name__ == "__main__":
    love()
