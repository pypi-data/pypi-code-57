import numpy as np
import sympy as sy
import math
import matplotlib.pyplot as plt

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


def plot_circle_dia(Voc,Ioc,Woc,Vsc,Isc,Wsc,Rating,Rotor_to_stator_loss_ratio,Scale):
    iocs = Ioc/Scale
    iscs = Isc/Scale
    

    
    
    isn = Isc * (Voc/Vsc)
    isns = isn/Scale
    rotor = Rotor_to_stator_loss_ratio

    npf = Woc/(math.sqrt(3)*Voc*Ioc)
    npfangle = math.acos(npf) #it is in radians

    px = iocs*math.sin(npfangle)
    py = iocs*math.cos(npfangle)


    lpf = math.acos(Wsc/(math.sqrt(3)*Vsc*Isc))
    
    qx = isns*math.sin(lpf)
    qy = isns*math.cos(lpf)

    m = (qy-py)/(qx-px)
    xsemi = (px**2 - py**2 - qx**2 - qy**2 +2*py*qy )/(2*(px-qx))
    r = xsemi - px

    the = []


    for x in np.arange(0,np.pi,np.pi/777):  #msd
        the.append(x)

    costhe = np.cos(the)
    sinthe = np.sin(the)

    lpf = math.acos(Wsc/(math.sqrt(3)*Vsc*Isc))

    
    aa = np.multiply(r,costhe)
    bb = np.multiply(r,sinthe)
    
    a = [i+xsemi for i in aa]
    b = [j + py for j in bb]


    fig, ax = plt.subplots()
    l0=ax.plot(a,b,label='Circle')
    l1=ax.plot([0,px],[0,py],label = 'No load Current')
    l2=ax.plot([px,qx],[py,qy],label='Output line')
    l3=ax.plot([px,2*xsemi],[py,py],label='No load Losses')
    l4=ax.plot([qx,qx],[0,qy],label='Losses')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    rmath = (rotor * py + qy)/(rotor + 1)
    l5=ax.plot([px,qx],[py,rmath],label='Torque Line')

    wsn = Wsc*isn*isn/(Isc*Isc)
    powerscale = wsn / qy
    qe = Rating/powerscale
    ey = qy + qe

    ax.plot([qx,qx],[qy,ey],label='_nolegend_')
    ax.plot([px,qx],[py+qe,ey],'--',label='_nolegend_')
    
    k1 = (qy+ qe - m*qx);
    k2 = (2*m*(k1 - py)-2*xsemi)/(1+m*m)
    k3 = (xsemi*xsemi + (k1 - py)*(k1 - py) - r*r)/(1+m*m)

    cex = (-k2 - math.sqrt(k2*k2 - 4*k3))/2
    cey = (m* cex + k1)

    l6=ax.plot([0,cex],[0,cey],label='Full Load Current')

    ocex = cex 
    ocey = m * cex - m*qx + qy


    #max output
    k4 = (px+qx+m*py+m*qy)/(2*m)
    k5 = (2*m*py - 2*m*m*xsemi - 2*m*k4)/(m*m+1)
    k6 = (m*m*xsemi*xsemi + m*m*(py - k4)*(py - k4) - m*m*r*r)/(m*m +1)
    mox = (-k5-math.sqrt(k5*k5 -4*k6))/2
    moy = (-mox/m )+k4
    moox = mox
    mooy = m*mox - m*qx + qy

    l7=ax.plot([mox,moox],[moy,mooy],label='Max output')

    
#max torque

    rsx = qx
    n = (rmath - py)/(rsx - px)
    k7 = (px + rsx + n*py + n*rmath)/(2*n) 
    k8 = (2*n*py - 2*n*k7 - 2*n*n*xsemi)/(n*n +1)
    k9 = (n*n*xsemi*xsemi + n*n*(py - k7)*(py - k7) - n*n*r*r)/(n*n +1)
    tox = (-k8-(math.sqrt((k8*k8 -4*k9))))/2
    toy = (-tox/n )+k7
    toox = tox
    tooy = n*tox + (py + rmath - n*px - n*rsx)/2 
    maths = n*cex-n*px+py
    ba = ocey-maths
    fldslp = ba/(cey-maths)

    l8=ax.plot([tox,toox],[toy,tooy],label='Max torque')


    maxt = (toy - tooy)*powerscale
    moxo = (moy - mooy)*powerscale
    fulli = (math.sqrt(cex*cex + cey*cey))*Scale
    maxi = (r+iocs*math.cos(npfangle))*powerscale
    efficency = ((cey-ocey)/cey) *100
    powerfactor = cey/(math.sqrt(cex**2 + cey**2))
    startingtorque = (qy-rmath)*powerscale
    torqueFullLoad = (cey-iocs*math.cos(npfangle))*powerscale

    h, l = ax.get_legend_handles_labels()


    fig.legend([h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7],h[8]], [l[0], l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8]], loc=1)

    plt.show()

    res = [maxt,moxo,fulli,maxi,efficency,powerfactor,startingtorque,torqueFullLoad]
    return res

































    















