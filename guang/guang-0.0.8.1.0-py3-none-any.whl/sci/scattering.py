from scipy import sin, pi, cos, real, arcsin, arccos, diff, interpolate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)  # 显示中文


def theta_s(theta_i, p, m):
    '''输入的theta 是度数不是弧度,得到的是偏转角'''
    theta_i = theta_i * pi / 180
    theta_r = arcsin(sin(theta_i) / m)
    ths = (2 * p * theta_r - 2 * theta_i - (p - 1) * pi)
    ths = real(ths)
    res = ths * 180 / pi
    return res


def sgn(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


def trans2thetap(theta_s, p):
    ''' 将偏转角转换为散射角 ,单位是角度，不是弧度
        p的范围需要≥0
    '''
    k_p = (180 - theta_s) // (2 * 180)
    q = sgn(theta_s + 360 * k_p)
    if q == 0:
        return theta_s
    theta_p = (theta_s + 2 * 180 * k_p) / q
    return theta_p


def find_theta_i(ths, p, m, error=1e-12):
    flag = 0  # 判断是否进行两次求值

    if p == 0 or p == 1:  # 0阶
        theta_min, theta_max = 0, 90

    else:
        # p=2时， 当 1<m<2.5时， 散射角真实位置处于 -0 ~ -360°
        theta_e = arccos(np.sqrt((m**2 - 1) / (p**2 - 1))) * 180 / pi
        theta_end = trans2thetap(theta_s(90, p, m), p)
        # 如果小于两者中更小的角度，则返回空
        if ths < theta_end and ths < trans2thetap(theta_s(theta_e, p, m), p):
            return []
        #         print('极值点:入射角{:.2f},入射角对应散射角{:.2f},thetaend:{:.2f}'.format(theta_e,theta_s(theta_e,p,m),theta_end))
        # 那么单值情况便只会出现在thetaend ~ 180° 散射角区域
        # 所以可以设定 当 theta < thetaend ，返回空
        #         if ths < theta_end : # 这一句可以直接将上面一句的and 改为 or
        #             return []        # 但，我想把这句注释掉，我想看到多条光线

        #        y_peak = trans2thetap(theta_s(theta_e,p,m),p) # 二阶光线的最高点，实际确实散射角最小位置
        theta_min = 1e-10
        theta_max = theta_e  # 这句话是不是有问题,应该是下面这句?
        #         theta_max = arccos(np.sqrt((m**2-1)/(p**2-1))) * 180/pi
        flag = 1

    temp_min = trans2thetap(theta_s(theta_min, p, m), p) - ths
    temp_max = trans2thetap(theta_s(theta_max, p, m), p) - ths

    # 二分求解
    while abs(temp_max - temp_min) > error:

        theta_mean = (theta_min + theta_max) / 2
        temp_mean = trans2thetap(theta_s(theta_mean, p, m), p) - ths
        if temp_mean * temp_max < 0:
            theta_min = theta_mean
            temp_min = temp_mean

        else:
            theta_max = theta_mean
            temp_max = temp_mean

    res = [theta_mean]
    if flag == 1:

        theta_min = theta_e
        theta_max = 90

        temp_min = trans2thetap(theta_s(theta_min, p, m), p) - ths
        temp_max = trans2thetap(theta_s(theta_max, p, m), p) - ths
        if temp_max * temp_min > 0:
            return res
        # 二分求解
        while abs(temp_max - temp_min) > error:

            theta_mean = (theta_min + theta_max) / 2
            temp_mean = trans2thetap(theta_s(theta_mean, p, m), p) - ths
            if temp_mean * temp_max < 0:
                theta_min = theta_mean
                temp_min = temp_mean

            else:
                theta_max = theta_mean
                temp_max = temp_mean

        res.append(theta_mean)

    return res


def phase(theta_i, alpha, p, m):
    '''输入的theta 是角度不是弧度'''
    theta_i = np.array(theta_i)
    theta_i = theta_i * pi / 180
    if p != 0:
        theta_i[theta_i > real(arcsin(m))] = None

    #     costheta_r = np.sqrt(1 - np.sin(theta_i/m)**2)
    theta_r = real(arcsin(sin(theta_i) / m))  # 这里默认给出复数形式，取实数部分，

    return 2 * alpha * (cos(theta_i) - p * m * cos(theta_r))


from scipy import diff


def phase_diff(ths, alpha, p0, p1, m):
    '''计算相位差'''

    theta_i0 = find_theta_i(ths, p0, m)
    theta_i1 = find_theta_i(ths, p1, m)

    try:
        if theta_i1[1]:
            theta_i1 = [theta_i1[1]]  # 这里如果find_theta_i返回两个解,选择第一个或者第二个
            # 而从Mie解中发现,这里对应的应该是第二个解
    except:
        pass
    theta_i0, theta_i1

    phase0 = phase(theta_i0, alpha, p0, m)
    phase1 = phase(theta_i1, alpha, p1, m)
    return phase1 - phase0


####################################
#        p0+p1 or p0 + p2
####################################
def pd_output(p, m, alpha):
    N = 500
    PD = np.zeros(N)

    if p == 1:
        theta_end = trans2thetap(theta_s(90, p, m), p)
        theta = np.linspace(1e-10, theta_end - 1e-10, N)
        theta_range = theta_end
    else:
        ths_end = arccos(np.sqrt((m**2 - 1) / (p**2 - 1))) * 180 / pi  # 彩虹角位置
        theta_end = trans2thetap(theta_s(ths_end, p, m), p)
        theta = np.linspace(theta_end + 1e-10, 180, N)
        theta_range = 180 - theta_end

    print(theta_end)

    dtheta = theta_range / (N - 1)
    i = 0
    for ths in theta:
        # result = find_theta_i(ths, p, m, error=1e-12)
        pd = phase_diff(ths, alpha, 0, p, m)
        PD[i] = pd
        i += 1

    # 输出: 散射角,相位差, 散射角, 相位差频率
    return (theta, PD, theta[1:], abs(diff(PD)) / (2 * pi * dtheta))


def frequency(p, m, theta_begin, alpha, dthe=3):
    Nu = np.zeros(len(alpha))
    if p == 1:
        flag_p = 1
        fName = '单角度数据//m={:.2f},p={:d},theta={:.2f}'.format(m, p, theta_begin)
        theta_max = trans2thetap(theta_s(90, p, m), p)
        # ************************************************************************************
        #         print('p={},m={:.2f},theta={},theta_max={:.2f}'.format(p,m,theta_begin,theta_max))
        # ************************************************************************************
        if theta_begin > theta_max:
            flag_p = 0
            # *********************************************************
    #             print('该角度范围无对应{}阶光线'.format(p))
    # *********************************************************

    if p == 2:
        flag_p = 2
        fName = '单角度数据//m={:.2f},p={:d},theta={:.2f}'.format(m, p, theta_begin)
        theta_e = arccos(np.sqrt((m**2 - 1) / (p**2 - 1))) * 180 / pi
        theta_min = min(trans2thetap(theta_s(90, p, m), p),
                        trans2thetap(theta_s(theta_e, p, m), p))
        print('p={},m={:.2f},theta={},theta_min={:.2f}'.format(
            p, m, theta_begin, theta_min))
        if theta_begin < theta_min:
            flag_p = 0
            # *********************************************************
    #             print('该角度范围无对应{}阶光线'.format(p))
    # *********************************************************

    if flag_p:
        for i_alpha in range(len(alpha)):
            pdiff = []

            # 注意！！！！这里如果直接求导得到频率必须是将散射角间隔分为恰好一度！
            M = 2

            ths = np.linspace(theta_begin, theta_begin + dthe, M)
            for _ in ths:
                pdiff.append(phase_diff(_, alpha[i_alpha], 0, p, m))

            pdiff = np.array(pdiff).reshape(1, M)  # 将列表转为数组
            pdd = abs(diff(pdiff))  # 求导，斜率取正

            Nu[i_alpha] = pdd[0][0] / (2 * pi * dthe / (M - 1))
        return Nu, fName


def get_k1k2(theta_1_begin, theta_2_begin, dthe1, dthe2, p1=1, p2=1):
    """i1"""
    temp_x, temp_y_1, temp_y_2, temp_y_3 = [], [], [], []
    # 将找到极值的精确角度区间给theta1 theta2
    # **********************************************************
    theta1, theta2 = theta_1_begin, theta_2_begin
    # **********************************************************
    for i in range(1, 100):
        for j in range(2):
            if j == 0:
                theta = theta1
                p = p1
                temp_m = 1.3 + i * 0.001
                Nu1, _ = frequency(p,
                                   temp_m,
                                   theta_begin=theta,
                                   alpha=[1],
                                   dthe=dthe1)
                temp_x.append(temp_m)
                temp_y_1.append(Nu1[0])  # 以浮点数形式存放,而不是array
            if j == 1:
                theta = theta2
                p = p2
                # print("p=",p,"m=",temp_m,"theta_begin=",theta,"alpha=", [1],"dthe=",dthe2)
                Nu2, _ = frequency(p,
                                   temp_m,
                                   theta_begin=theta,
                                   alpha=[1],
                                   dthe=dthe2)
                temp_y_2.append(Nu2[0])  # 以浮点数形式存放,而不是array
    k1 = interpolate.interp1d(temp_x, temp_y_1, kind='cubic')
    k2 = interpolate.interp1d(temp_x, temp_y_2, kind='cubic')
    return k1, k2


def predict(v1, v2, k1, k2, m_min=1.301, m_max=1.399):
    """输入以及计算好m区间和角度区间的插值函数k1, k2
    然后给出v1, v2计算alpha,m"""
    func = lambda x: v1 * k2(x) - v2 * k1(x)

    def dichotomy2(f, xleft, xright, error=1e-12):
        fxleft = f(xleft)
        fxright = f(xright)

        if fxleft * fxright > 0:
            print('当前区域无解,返回右端点函数值\n')
            return xright
        while abs(xright - xleft) > error:
            xmean = (xleft + xright) / 2
            fxmean = f(xmean)
            if fxleft * fxmean < 0:
                xright = xmean
                fxright = fxmean
            else:
                xleft = xmean
                fxleft = fxmean
        return (xright + xleft) / 2

    m = dichotomy2(func, m_min, m_max)  # 1.30 ~ 1.35即可
    alpha1 = v1 / k1(m)
    alpha2 = v2 / k2(m)

    return alpha1, alpha2, m
