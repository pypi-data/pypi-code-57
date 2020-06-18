from guang.sci.fft import space2fre
import numpy as np
from numpy import pi, sin, cos, linspace
import plotly.express as px
import streamlit as st


def example_func(x_min, x_max):
    x = np.linspace(x_min, x_max, 1000)
    f1, f2, f3 = 0.1, 2, 8
    w1, w2, w3 = 2 * pi * f1, 2 * pi * f2, 2 * pi * f3
    y = 2 * sin(w1 * x) + 0.8 * sin(w2 * x)  # + 0.2 * sin(w3*x)
    return x, y


def randFunc(N, F, A):
    x = np.linspace(-3, 4, N)
    y = np.zeros(N)
    for f, a in zip(F, A):
        w = 2 * np.pi * f
        y += np.sin(w * x) * a
    return x, y


def showLatexFunc(F, A):
    y = f" $f(x)=$ "
    for f, a in zip(F, A):
        w = f"$2\pi\cdot{f}$"
        y += f"{a}$\cdot\sin$ ({w} $x$) + "  #f"$\\sin({w}x) a$"
    st.write(f"{y[:-2]} \n    $x\\in[-3, 4]$")


def tutorial():
    global example_func
    x, y = example_func(-10, 10)
    fig = px.line(x=x, y=y)
    "原始函数："
    r"$2 \cdot sin(2\pi\cdot 0.1  x) + 0.8 * sin(2\pi\cdot 2 x)$"
    st.write(fig)

    fre_y = np.fft.fft(y)
    X = np.arange(len(fre_y))
    fig2 = px.line(x=X,
                   y=np.abs(fre_y),
                   labels={
                       'x': '_Frequency',
                       'y': 'Amplitude'
                   },
                   range_x=(-50, 1050))
    "直接对函数进行fft"
    fig2

    fre_y_shift = np.fft.fftshift(fre_y)
    fig3 = px.line(x=X,
                   y=np.abs(fre_y_shift),
                   labels={
                       'x': '_Frequency',
                       'y': '_Amplitude'
                   },
                   range_x=(-50, 1050))
    "fftshift移动为中心对称："
    fig3
    r""" 
    这是我们还没有给它设置含坐标刻度。它的很坐标的意义是频率值，
    中心点的频率为0，最右侧的频率应该是这个频率空间的最大频率值（听上去像废话），
    左边是跟右边对称的。那么最重要的就是确定出这个频率空间的最大频率是多少。  
    而这个最大频率是由原始空间（坐标空间）x决定。频率=1/周期，最大频率由最小周期所确定，而
    最小周期自然是由空间的最小间隔（或者说采样间隔）决定。  
    我们的x一共有1000个值，
    分布-10 ~ 10之间，那么x的最小间隔$\delta x =\frac{x_{max}-x_{min}}{N-1}= \frac{20}{1000-1}$，
    那么想象下，2个振荡周期最少需要几个坐标点？
    """
    r"""
    思考完毕，两个周期最小需要5个点。 想象一个锯齿函数~   
    那么N个点可以承载最多$\frac{N-1}{2}$个周期. 那时一个周期的距离就是两倍最小间隔$2\delta x$ . 
    这时我们就有： 
    $$
    T = 2\delta x,\ \ 
    f_{max} = \frac{1}{T} = \frac{1}{2\delta x}=\frac{N-1}{2(x_{max}-x_{min})}
    $$
    同样，对于频率f而言，有：
    $$
    \delta f = \frac{2f_{max}}{N-1}
    $$
    """

    x_max = x.max()
    x_min = x.min()
    N = len(x)
    delta_x = (x_max - x_min) / (N - 1)

    f_max = 1 / (2 * delta_x)
    delta_f = 2 * f_max / (N - 1)
    r"这里计算得到$f_{max}=\frac{1}{2\cdot\delta x}=$", f_max
    r"$\delta f=$", delta_f
    if N % 2 == 0:
        fre_x = np.linspace(-f_max, f_max, N) - delta_f / 2
    else:
        fre_x = np.linspace(-f_max, f_max, N)
    fig4 = px.line(
        x=fre_x,
        y=np.abs(fre_y_shift),
        labels={"x": "frequency"},
    )
    fig4
    """ 
    上图可以看到在频率为 0附近 以及 2附近存在两个峰，而这两个频率就是一开始时我们所设置的f1 和 f2 ,
    分别为0.1 和 2 x轴的意义弄清楚了。而y轴，对应的当然是振幅啦，只是我们需要进行一个规范化的操作：
    2*abs(fre_y_shift)/N-1
    """

    amplitude_y = 2 * np.abs(fre_y_shift) / (len(x) - 1)
    fig5 = px.line(x=fre_x,
                   y=amplitude_y,
                   labels={
                       "x": "frequency",
                       "y": "amplitude"
                   })
    fig5


def test_fft():
    option = st.sidebar.selectbox("共有几个频率呢", np.arange(10))
    max_fre = 50
    f = np.arange(option)
    A = np.arange(option)
    for i in range(option):
        f[i] = st.sidebar.slider(f"频率{i}", 0, max_fre, 1)
        A[i] = st.sidebar.slider(f"振幅{i}", 0, 20, 5)

    N = st.sidebar.slider(f"函数采样数", 10, 10000, 1000)
    x, y = randFunc(N, f, A)
    fig0 = px.line(x=x, y=y)
    st.write(fig0)
    showLatexFunc(f, A)
    fre, amp = space2fre(x, y)

    fig = px.line(x=fre[:, 0],
                  y=amp[:, 0],
                  labels={
                      "x": "Frequency",
                      "y": "Amplitude"
                  })
    st.write(fig)


if st.sidebar.checkbox("Fundamental教程"):
    tutorial()

"---"
test_fft()
