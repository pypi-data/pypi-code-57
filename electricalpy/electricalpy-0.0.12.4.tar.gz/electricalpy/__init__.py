import numpy as np
import sympy as sy

def series(series_elements):
    temp = 0
    for i in range(0,len(series_elements)):
        temp = temp + series_elements[i]
    return temp


def parallel(parallel_elements):
    tempp = 0;
    for j in range(0,len(parallel_elements)):
        tempp = tempp + 1/(parallel_elements[j])
    return (1/(tempp))

def to_star(ab_ba_ca):
    ab=ab_ba_ca[0]
    bc=ab_ba_ca[1]
    ca=ab_ba_ca[2]
    
    ra = (ab*ca)/(ab+bc+ca)
    rb = (ab*bc)/(ab+bc+ca)
    rc = (ca*bc)/(ab+bc+ca)
    
    return [ra,rb,rc]


def to_delta(a_b_c):
    ra = a_b_c[0]
    rb = a_b_c[1]
    rc = a_b_c[2]

    rbc = rb + rc + (rb*rc)/ra
    rac = ra + rc + (ra*rc)/rb
    rab = ra + rb + (ra*rb)/rc

    return [rab, rbc, rac]

def to_rectangular(mag_angl):
    mag = mag_angl[0]
    ang = mag_angl[1]

    x = np.around(mag*np.cos(ang*np.pi/180))
    y = np.around(mag*np.sin(ang*np.pi/180))

    return complex(x,y)

def to_polar(x_y):
    r = np.around(abs(x_y))
    theta = np.around(np.angle(x_y,deg=True))
    return([r,theta])
    


def RH(coeffients):
    e = []
    o = []
    
    lorg = len(coeffients)
    #coeffients.append(0)
    if(lorg%2!=0):
        coeffients.append(0)
    l = len(coeffients)
    for i in range(0,l):
        if (i%2 ==0):
            e.append(coeffients[i])
        else:
            o.append(coeffients[i])

    ranges = lorg-2
    w, h = len(e),ranges
    res = [[0 for x in range(w)] for y in range(h)]
    e.append(0)
    o.append(0)

    for j in range(0,h):
        for k in range(0,w):
            res[j][k]=((o[0]*e[k+1])-(e[0]*o[k+1]))/o[0]
        e=o
        o = res[j]
        o.append(0)

    r,useless = np.shape(res)
    result = []
    for l in range(0,r):
        if(res[l][0]<=0):
            output = "unstable/marginally stable"
            break
        else:
            output = "stable"
    return output,res

def rms(function,limit_1,limit_2,period,degree = True):


    if(degree):
        limit_1 = limit_1 * sy.pi/180
        limit_2 = limit_2 * sy.pi/180
        period = period * sy.pi/180


    
    x = sy.Symbol('x')

    aarms = sy.sqrt((1/period) * sy.integrate(function*function,(x,limit_1,limit_2)))
    
    return aarms

def avg(function,limit_1,limit_2,period,degree = True):
    if(degree):
        limit_1 = limit_1 * sy.pi/180
        limit_2 = limit_2 * sy.pi/180
        period = period * sy.pi/180    
    x = sy.Symbol('x')
    ravg = 1/(period)*sy.integrate(function,(x,limit_1,limit_2))
    return (ravg)

