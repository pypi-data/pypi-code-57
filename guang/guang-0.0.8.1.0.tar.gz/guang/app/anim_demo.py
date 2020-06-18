import streamlit as st
import numpy as np
import plotly.graph_objects as go
from guang.app.compose.animation import Draw2D, Draw3D, Traces2d, lorenz_Traces

option = st.sidebar.selectbox('Which animation do you want to draw?',
                              ['2d', '3d'])
'You have selected:', option

if option == "3d":
    k = st.sidebar.slider('how many lines?', 1, 10, 5)
    all_step = st.sidebar.slider('how many steps?', 500, 5000, 900)
    total_frames = st.sidebar.slider('total frames', 100, 1000, 200)
    period = st.sidebar.slider('period', 1, 100, 5)
    period /= 100

    @st.cache(suppress_st_warning=True)
    def drawing(all_step, k, total_frames, period):
        draw3d = Draw3D()
        draw3d.Traces = lorenz_Traces(x0=5,
                                      y0=6,
                                      z0=10,
                                      lambd=10,
                                      k=k,
                                      all_step=all_step)
        fig = draw3d.anima(total_frames=total_frames, period=period)
        return fig

    if st.checkbox("3D rendering"):
        fig = drawing(all_step, k, total_frames, period)
        st.plotly_chart(fig)

if option == "2d":

    all_step = st.sidebar.slider('all step?', 1000, 6000, 1500)
    total_frames = st.sidebar.slider('total frames', 100, 1000, 200)
    period = st.sidebar.slider('period', 1, 100, 5)
    period /= 100

    @st.cache(suppress_st_warning=True)
    def drawing(all_step, total_frames, period, width, height):
        draw2d = Draw2D()
        x = np.linspace(0, 20, all_step)[..., None]
        y = np.sin(x)
        Trace = []
        Trace.append(np.concatenate((x, y), axis=1))

        draw2d.Traces = Trace
        fig = draw2d.anima(total_frames=total_frames,
                           period=period,
                           width=990,
                           height=400)
        return fig

    if st.checkbox("2D rendering"):
        fig = drawing(all_step=all_step,
                      total_frames=total_frames,
                      period=period,
                      width=990,
                      height=400)
        st.plotly_chart(fig)
