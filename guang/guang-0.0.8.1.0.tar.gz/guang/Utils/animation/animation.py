import plotly.graph_objects as go
import numpy as np
from guang.interesting import Lorenz
from guang.Utils.plotly import Scatter3d
from guang.Utils.animation.utils import ExtremeValue


def getRange(x, dx=0.02):
    delta = np.max(x) - np.min(x)
    delta = delta * dx
    return np.min(x) - delta, np.max(x) + delta


def lorenz_Traces(x0=1,
                  y0=3,
                  z0=5,
                  lambd=0.01,
                  k=3,
                  t_start=0,
                  t_end=10,
                  all_step=900):

    t = np.linspace(t_start, t_end, all_step)
    Traces = []
    for i in range(k):
        trace = Lorenz.Trace(t=t,
                             xyz=[
                                 x0 + lambd * np.random.rand(),
                                 y0 + lambd * np.random.rand(),
                                 z0 + lambd * np.random.rand()
                             ])
        Traces.append(trace)
    return Traces


class Draw3D:
    def __init__(self):
        self.Traces = []
        self.initial_data = {}

    def get_extrem(self):
        Value = ExtremeValue()
        for trace in self.Traces:
            x, y, z = trace[:, 0], trace[:, 1], trace[:, 2]
            xm, xM = getRange(x)
            ym, yM = getRange(y)
            zm, zM = getRange(z)
            xm, ym, zm = Value.get_min(x=xm, y=ym, z=zm)
            xM, yM, zM = Value.get_max(x=xM, y=yM, z=zM)
        return xm, xM, ym, yM, zm, zM

    def get_frames(self, total_frames=100, period=1):
        """
        :param total_frames: total frames
        :param period: value interval:(0, 1] means the percentage of the total points.
        """
        self.k = len(self.Traces)
        N = len(self.Traces[0][:, 0])
        step = N // total_frames
        i_start, i_end = 0, 0
        counts_period = int(N * period)
        frames = []
        for i in range(total_frames):
            i_end += step
            i_start = i_end - counts_period if i_end > counts_period else 0
            data = []

            for trace in self.Traces:
                x, y, z = trace[:, 0], trace[:, 1], trace[:, 2]
                data_x = x[i_start:i_end]
                data_y = y[i_start:i_end]
                data_z = z[i_start:i_end]
                data.append(
                    go.Scatter3d(x=data_x,
                                 y=data_y,
                                 z=data_z,
                                 mode="lines+markers",
                                 line=dict(color=None, width=1.5),
                                 marker=dict(size=1.5,
                                             color=z,
                                             colorscale='Viridis')))

            if i == 0:
                self.initial_data.setdefault('data', data)
            frames.append(
                go.Frame(
                    data=data,
                    traces=[i for i in range(self.k)
                            ]  ####THIS IS THE LINE THAT MUST BE INSERTED
                ))

        return frames

    def get_layout(self):
        xm, xM, ym, yM, zm, zM = self.get_extrem()
        layout = go.Layout(
            width=780,
            height=780,
            scene={
                'xaxis': {
                    'range': [xm, xM],
                    "nticks": 10,
                    'autorange': False,
                    "zeroline": False
                },
                # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                'yaxis': {
                    'range': [ym, yM],
                    "nticks": 10,
                    'autorange': False,
                    "zeroline": False
                },
                # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                'zaxis': {
                    'range': [zm, zM],
                    "nticks": 10,
                    'autorange': False,
                    "zeroline": False
                },
                # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                'aspectmode': 'cube',
            },
            title="Lorenz Curve",
            hovermode="closest",
            updatemenus=[
                dict(type="buttons",
                     buttons=[
                         dict(label="Play",
                              method="animate",
                              args=[
                                  None,
                                  dict(frame=dict(duration=20, redraw=True),
                                       transition=dict(duration=0),
                                       fromcurrent=True,
                                       mode='immediate')
                              ])
                     ])
            ])
        return layout

    def anima(self, total_frames=200, period=0.05):
        frames = self.get_frames(total_frames=total_frames, period=period)
        data = self.initial_data['data']
        fig = go.Figure(data=data, layout=self.get_layout(), frames=frames)
        return fig


class Draw2D:
    def __init__(self):
        self.Traces = []
        self.initial_data = {}

    def get_extrem(self):
        Value = ExtremeValue()
        for trace in self.Traces:
            x, y = trace[:, 0], trace[:, 1]
            xm, xM = getRange(x)
            ym, yM = getRange(y)

            xm, ym = Value.get_min(x=xm, y=ym)
            xM, yM = Value.get_max(x=xM, y=yM)
        return xm, xM, ym, yM

    def get_frames(self, total_frames=100, period=1):
        """
        :param total_frames: total frames
        :param period: value interval:(0, 1] means the percentage of the total points.
        """
        self.k = len(self.Traces)

        N = len(self.Traces[0][:, 0])
        step = N // total_frames
        i_start, i_end = 0, 0
        counts_period = int(N * period)
        frames = []
        for i in range(total_frames):
            i_end += step
            i_start = i_end - counts_period if i_end > counts_period else 0
            data = []

            for trace in self.Traces:
                x, y = trace[:, 0], trace[:, 1]
                data_x = x[i_start:i_end]
                data_y = y[i_start:i_end]
                data.append(
                    go.Scatter(x=data_x,
                               y=data_y,
                               mode="lines",
                               line=dict(color=None, width=2)))

            if i == 0:
                self.initial_data.setdefault('data', data)
            frames.append(
                go.Frame(
                    data=data,
                    traces=[i for i in range(self.k)
                            ]  #THIS IS THE LINE THAT MUST BE INSERTED
                ))
        return frames

    def get_layout(self,
                   width=980,
                   height=880,
                   duration=10,
                   title="Lorenz X-Y 2D Curve",
                   redraw=False,
                   mode='immediate'):
        xm, xM, ym, yM = self.get_extrem()

        # height = int(width* (yM-ym)/(xM-xm)) + 100
        layout = go.Layout(
            width=width,
            height=height,
            xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
            yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
            title=title,
            hovermode="closest",
            updatemenus=[
                dict(type="buttons",
                     buttons=[
                         dict(label="Play",
                              method="animate",
                              args=[
                                  None,
                                  dict(frame=dict(duration=duration,
                                                  redraw=redraw),
                                       transition=dict(duration=0),
                                       fromcurrent=True,
                                       mode=mode)
                              ])
                     ])
            ])
        return layout

    def anima(self, total_frames=200, period=0.05, width=990, height=900):
        frames = self.get_frames(total_frames=total_frames, period=period)
        data = self.initial_data['data']
        layout = self.get_layout(width=width, height=height)
        fig = go.Figure(data=data, layout=layout, frames=frames)
        return fig


def Traces2d(r=10, all_step=1000):

    theta = np.linspace(0, 2 * np.pi, all_step)[..., None]
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    Trace = []
    Trace.append(np.concatenate((x, y), axis=1))
    Trace.append(np.concatenate((theta + r, x), axis=1))
    Trace.append(np.concatenate((theta - r, y), axis=1))
    return Trace


if __name__ == "__main__":
    draw2d = Draw2D()
    draw2d.Traces = Traces2d(r=10)
    fig = draw2d.anima(total_frames=200, period=1)
    fig.show()

    # draw3d = Draw3D()
    # draw3d.Traces = lorenz_Traces(x0=5, y0=6, z0=10, lambd=10,
    #                               k=5, all_step=900)
    # ---------------------------------------------------- option start
    # xm, xM, ym, yM, zm, zM = draw3d.get_extrem()
    # draw3d.initial_data =  [go.Scatter3d(x=[xm], y=[ym], z=[zm]),
    #                     go.Scatter3d(x=[xM], y=[yM], z=[zM]),
    #                     go.Scatter3d(x=[xm], y=[yM], z=[zm]), ]
    # ---------------------------------------------------- option end

    # fig = draw3d.anima(total_frames=200, period=0.05)
    # fig.show()
