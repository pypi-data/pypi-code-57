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







#2 port



def z_to_y(z_parameters):
    det_ = np.linalg.det(z_parameters)

    z11 = z_parameters[0][0]
    z12 = z_parameters[0][1]
    z21 = z_parameters[1][0]
    z22 = z_parameters[1][1]

    y11 = z22/det_
    y12 = -z12/det_
    y21 = -z21/det_
    y22 = z11/det_

    res = [[y11,y12],[y21,y22]]
    return res

def z_to_t(z_parameters):
    det = np.linalg.det(z_parameters)

    z11 = z_parameters[0][0]
    z12 = z_parameters[0][1]
    z21 = z_parameters[1][0]
    z22 = z_parameters[1][1]

    a = z11/z21
    b = det/z21
    c = 1/z21
    d = z22/z21

    res = [[a,b],[c,d]]
    return res

def z_to_h(z_parameters):
    det = np.linalg.det(z_parameters)

    z11 = z_parameters[0][0]
    z12 = z_parameters[0][1]
    z21 = z_parameters[1][0]
    z22 = z_parameters[1][1]

    h11 = det/z22
    h12 = z12/z22
    h21 = -z21/z22
    h22 = 1/z22

    res = [[h11,h12],[h21,h22]]
    return res

def y_to_z(y_parameters):
    det = np.linalg.det(y_parameters)

    y11 = y_parameters[0][0]
    y12 = y_parameters[0][1]
    y21 = y_parameters[1][0]
    y22 = y_parameters[1][1]

    z11 = y22/det
    z12 = -y21/det
    z21 = -y21/det
    z22 = y11/det

    res = [[z11,z12],[z21,z22]]
    return res


def t_to_z(t_parameters):
    det = np.linalg.det(t_parameters)

    a = t_parameters[0][0]
    b = t_parameters[0][1]
    c = t_parameters[1][0]
    d = t_parameters[1][1]

    z11 = a/c
    z12 = det/c
    z21 = 1/c
    z22 = d/c

    res = [[z11,z12],[z21,z22]]
    return res
def h_to_z(h_parameters):
    det = np.linalg.det(h_parameters)

    h11 = h_parameters[0][0]
    h12 = h_parameters[0][1]
    h21 = h_parameters[1][0]
    h22 = h_parameters[1][1]

    z11 = det/h22
    z12 = h12/h22
    z21 = h21/h22
    z22 = 1/h22

    res = [[z11,z12],[z21,z22]]
    return res

def y_to_t(y_parameters):
    r1 = y_to_z(y_parameters)
    res = z_to_t(r1)
    return r1
def y_to_h(y_parameters):
    r1 = y_to_z(y_parameters)
    return  (z_to_h(r1))

def t_to_y(t_parameters):
    r1 = t_to_z(t_parameters)
    return(z_to_y(r1))
def t_to_h(t_parameters):
    r1 = t_to_z(t_parameters)
    return(z_to_h(r1))
def h_to_t(h_parameters):
    r1 = h_to_z(h_parameters)
    return(z_to_t(r1))
def h_to_y(h_parameters):
    r1 = h_to_z(h_parameters)
    return(z_to_h(r1))




























    















