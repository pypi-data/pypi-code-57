import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import meshgrid, linspace, pi, e, sin, cos

# 绘制2D图像
def draw_2D(function,x_min=-10,x_max=10,xlabel='x',ylabel='y',definition=100):
    '''
    绘制一元函数图像（2D）
    :param function: 函数
    :param x_min: 函数定义域的最小值
    :param x_max: 函数定义域的最大值
    :param xlabel: x轴名称
    :param ylabel: y轴名称
    :param definition: 精确度
    '''
    x = linspace(x_min,x_max,definition)
    y = function(x)
    plt.plot(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def draw_2D_list(function_list,domain_list,ylim,xlabel='x',ylabel='y'):
    '''
    绘制一元函数图像（2D）
    :param function_list: 函数列表
    :param domain_list: 定义域列表，示例：[array(linspace(-5,5,100)),array(linspace(-7,5,100))]
    :param ylim: y轴范围，比如：(-10,10)
    :param xlabel:x轴名称
    :param ylabel:y轴名称
    '''
    for domain, function in zip(domain_list,function_list):
        x = domain
        y = function(x)
        plt.plot(x,y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.ylim(ylim[0],ylim[1])
    plt.show()

# 绘制3D图像
def draw_3D(function,x_min=-10,x_max=10,y_min=-10,y_max=10,x_definition=100,y_definition=100):
    '''
    绘制二元函数图像（3D）
    :param function: 二元函数
    :param x_min: x轴最小值
    :param x_max: x轴最大值
    :param y_min: y轴最小值
    :param y_max: y轴最大值
    :param x_definition: x轴精度
    :param y_definition: y轴精度
    '''
    fig = plt.figure()
    ax = Axes3D(fig)
    x = linspace(x_min, x_max, x_definition)
    y = linspace(y_min, y_max, y_definition)
    X, Y = meshgrid(x, y)
    Z = function(X,Y)
    ax.plot_surface(X, Y, Z, cmap=plt.get_cmap('rainbow'))
    plt.show()

def f_2d(x):
    '''
    示例函数（标准正态分布），可按照此函数定义自己的函数，
    要求：必须接受一个arrray数组作为参数（定义域），并返回处理后的数组（对应的集合）
    '''
    return (1 / (pi * 2) ** 0.5) * (e ** (-0.5 * (x ** 2)))

def f_3d(x,y):
    '''
    示例函数，可按照此函数定义自己的函数，
    要求：必须接受两个arrray数组作为参数（定义域），并返回处理后的数组（对应的集合）
    '''
    return sin(x) + cos(y)