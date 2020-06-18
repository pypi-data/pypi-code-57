import plotly.graph_objects as go
import numpy as np
from guang.Utils.mathFunc import sawtooth


def slider_1D(x, y, color="#00CED1", linewidth=1, name="𝜈 = ", initial_step=1):
    """ create a 1D slider
    :param a list of array: x:  each menber is a one-dimention array
    :param a list of array: y: a list of f(x)

    Example

        from guang.Utils.mathFunc import sawtooth
        theta = np.linspace(0, 15, 1000)
        N = 10
        x, y = [], []
        for step in range(N):
            x.append(theta)
            y.append(sawtooth(step, theta))
        fig = slider_1D(x=x, y=y)
        fig.show()
    """
    # step 1 :Create a graph window fig, add all the graphs to fig, and set visible to False
    fig = go.Figure()

    for step in range(len(y)):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color=color, width=linewidth),  # --------------- 1
                name=name + str(step),  # --------------- 2
                x=x[step],  # --------------- 3
                y=y[step]  # --------------- 4
            ))

    # step 2： initial figure
    initial_step = initial_step  # --------------- 5
    fig.data[initial_step].visible = True

    # step 3: Each time an image is visible=True, the rest is False
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="restyle",
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [
        dict(
            active=initial_step,
            currentvalue={"prefix": "frequency: "},  # --------------- 6
            pad={"t": 50},  # --------------- (7)
            steps=steps)
    ]

    fig.update_layout(sliders=sliders)
    return fig


if __name__ == "__main__":

    theta = np.linspace(0, 15, 1000)
    N = 10
    x, y = [], []
    for step in range(N):
        x.append(theta)
        y.append(sawtooth(step, theta))
    fig = slider_1D(x=x, y=y)
    fig.show()
