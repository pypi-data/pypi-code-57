# Kornpob Bhirombhakdi 20200331

import numpy as np

def make_SIP(coef,x,y,startx=True):
    """
    Simple imaging polynomial (SIP) is a conventional method to describe non-linear variation in an image. Ref: https://fits.gsfc.nasa.gov/registry/sip/shupeADASS.pdf.
    ##########
    Assume a SIP model of order 2, i.e., Z = a0 + a1*X + a2*X**2.
    Typically, X is relative to SIP reference system whose origin is corresponding to (xref,yref) in the original image. Therefore, X = x - xref where (x,y) is an image pixel.
    Z is a quantity of interests. In aXe grism reduction, Z can be Y (as y = Y + yref) for trace, or wavelength.
    SIP coefficients are 2D with a given polynomial order. Assume the order is 3. Therefore, ai = ai0 + ai1*X' + ai2*Y' + ai3*X'**2 + ai4*X'*Y' + ai5*Y'**2 + ... + ai9*Y'**3.
    Note X is the leading term (this is specified by startx=True in make_SIP). Set startx=False otherwise.
    Note that X and X' might be different. For aXe reduction, (X',Y') = (xd,yd) as the source location from direct image.
    """
    if startx:
        xref,yref = x,y
    else:
        xref,yref = y,x
    n = len(coef)
    d = []
    px,py = 0,0
    a = [(px,py)]
    b = [(xref,yref)]
    p = 0
    q = True
    while(q):
        if px==0:
            p+=1
            px=p
            py=0
        else:
            px-=1
            py+=1
        a.append((px,py))
        b.append((xref,yref))
        if len(a)>=len(coef):
            q = False
    a,b = np.array(a),np.array(b)
    c = b**a
    c = np.sum(c[:,0]*c[:,1]*coef)
    d.append(c)
    d = np.array(d)
    return d 
