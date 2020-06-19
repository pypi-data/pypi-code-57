import lal
import lalsimulation as lalsim
import numpy as np
import warnings
import copy

class WaveformRotations(object):
    def __init__(self, times, hlms, frame, *args, **kwargs):
        """
        A class to perform rotations to modes
        times: 1d array of times
        hlms: dict of complex modes
            {(l,m):complex_modes}
        alpha0, thetaJN, phi0: angles to go from L (LAL) inertial frame to J inertial frame
        frame: str choices: ['inertial-L', 'inertial-J', 'coprec']

        if frame is 'inertial-L'
        required_args = ['alpha0', 'thetaJN', 'phi0']
        passed as kwargs

        if frame is 'coprec'
        required_args = ['alpha', 'beta', 'gamma']
        passed as kwargs

        modifies hlms in-place. To find out what frame you are in
        use self.frame.
        """
        frame_choices = ['inertial-L', 'inertial-J', 'coprec']
        if frame not in frame_choices:
            raise ValueError(f"input frame ({frame}) not in frame_choices ({frame_choices})")
        self.frame = frame

        if self.frame == 'inertial-L':
            required_args = ['alpha0', 'thetaJN', 'phi0']
            for r_arg in required_args:
                if r_arg not in kwargs.keys():
                    raise ValueError(f"{r_arg} not in {kwargs.keys()}")
            self.set_alpha0_thetaJN_phi0(kwargs['alpha0'], kwargs['thetaJN'], kwargs['phi0'])

        elif self.frame == 'coprec':
            required_args = ['alpha', 'beta', 'gamma']
            for r_arg in required_args:
                if r_arg not in kwargs.keys():
                    raise ValueError(f"{r_arg} not in {kwargs.keys()}")
            self.set_alpha_beta_gamma(kwargs['alpha'], kwargs['beta'], kwargs['gamma'])

        self.times = times
        self.hlms_original = copy.deepcopy(hlms)
        self.hlms = hlms

    def _rotate(self, times, hlms, r1, r2, r3):
        hlms_3col = convert_to_nrutils_dict(times, hlms)
        hlms_out_3col = {}
        hlms_out = {}
        for k in hlms_3col.keys():
            l, m = k
            hlms_out_3col[k] = rotate_wfarrs_at_all_times(l, m, hlms_3col, [r1, r2, r3])
            hlms_out[k] = hlms_out_3col[k][:,1] + 1.j * hlms_out_3col[k][:,2]

        return hlms_out

    def set_alpha0_thetaJN_phi0(self, alpha0, thetaJN, phi0):
        """
        set rotation angles to go from inertial-L to inertial-J frame
        """
        self.alpha0 = alpha0
        self.thetaJN = thetaJN
        self.phi0 = phi0

    def set_alpha_beta_gamma(self, alpha, beta, gamma):
        """
        set co-precessing angles
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def from_inertial_frame_to_j_frame(self):
        assert self.frame == "inertial-L"
        self.hlms = self._rotate(self.times, self.hlms, -self.alpha0 , -self.thetaJN, -self.phi0)
        self.frame = "inertial-J"

    def from_j_frame_to_coprecessing_frame(self, func='new', RoughDirection=None, RoughDirectionIndex=0):
        """
        func: str either 'old' or 'new'.
            'old' for nrutils, 'new' for scri
        RoughDirection: typically either [0,0,1] or [0,0,-1].
            If initial beta angle (thetaJN) is > pi/2 then should be [0,0,-1]
            otherwise use [0,0,1]
        """
        assert self.frame == "inertial-J"
        if func=='old':
            self.alpha, self.beta, self.gamma, self.X, self.Y, self.Z = \
                calc_coprecessing_angles(
                    self.hlms, domain_vals=self.times, return_xyz='all')
        elif func=='new':
            self.alpha, self.beta, self.gamma, self.X, self.Y, self.Z = \
                calc_coprecessing_angles_scri(
                    self.hlms, domain_vals=self.times, RoughDirection=RoughDirection, RoughDirectionIndex=RoughDirectionIndex)
        self.hlms = self._rotate(self.times, self.hlms, -self.gamma , -self.beta, -self.alpha)
        self.frame = "coprec"

    def from_inertial_frame_to_coprecessing_frame(self, func='new', RoughDirection=None, RoughDirectionIndex=0):
        """
        assumes we are in the LAL inertial frame i.e. L along z
        and transforms to the coprecessing frame.
        It first transforms to the J-frame and then
        performs the maximum emission direction calculation

        func: str either 'old' or 'new'.
            'old' for nrutils, 'new' for scri
        """
        assert self.frame == "inertial-L"
        self.from_inertial_frame_to_j_frame()

        if self.thetaJN > np.pi/2:
            RoughDirection = [0,0,-1]
        else:
            RoughDirection = [0,0,1]

        assert self.frame == "inertial-J"
        self.from_j_frame_to_coprecessing_frame(func=func, RoughDirection=RoughDirection, RoughDirectionIndex=RoughDirectionIndex)


    def from_coprecessing_frame_to_j_frame(self):
        """
        assumes we are in the coprecessing frame and performs inverse
        rotations to arrive back at the inerital LAL frame i.e. L along z.
        """
        assert self.frame == "coprec"
        self.hlms = self._rotate(self.times, self.hlms, self.alpha , self.beta, self.gamma)
        self.frame = "inertial-J"

    def from_j_frame_to_inertial_frame(self):
        assert self.frame == "inertial-J"
        if hasattr(self, 'alpha0') is False:
            raise ValueError("please set alpha0")
        if hasattr(self, 'thetaJN') is False:
            raise ValueError("please set thetaJN")
        if hasattr(self, 'phi0') is False:
            raise ValueError("please set phi0")
        self.hlms = self._rotate(self.times, self.hlms, self.phi0 , self.thetaJN, self.alpha0)
        self.frame = "inertial-L"

    def from_coprecessing_frame_to_inertial_frame(self):
        """
        assumes we are in the coprecessing frame and performs inverse
        rotations to arrive back at the inerital LAL frame i.e. L along z.
        """
        assert self.frame == "coprec"
        self.from_coprecessing_frame_to_j_frame()

        assert self.frame == "inertial-J"
        self.from_j_frame_to_inertial_frame()

def compute_L_to_J_angles(mass1, mass2, f_ref, inc, phiref, spin1x, spin1y, spin1z, spin2x, spin2y, spin2z):
    """
    from nrutils
    """
    _, _, _, thetaJN, alpha, phi_aligned, _ = lalsim.SimIMRPhenomPCalculateModelParametersFromSourceFrame(
        mass1*lal.MSUN_SI, mass2*lal.MSUN_SI,
        f_ref, phiref, inc,
        spin1x, spin1y, spin1z,
        spin2x, spin2y, spin2z,
        lalsim.IMRPhenomPv2_V)

    return thetaJN, alpha, phi_aligned


# Calculate Widger D-Matrix Element
def wdelement( ll,         # polar index (eigenvalue) of multipole to be rotated (set of m's for single ll )
               mp,         # member of {all em for |em|<=l} -- potential projection spaceof m
               mm,         # member of {all em for |em|<=l} -- the starting space of m
               alpha,      # -.
               beta,       #  |- Euler angles for rotation
               gamma ):    # -'
    """
    from nrutils
    """

    #** James Healy 6/18/2012
    #** wignerDelement
    #*  calculates an element of the wignerD matrix
    # Modified by llondon6 in 2012 and 2014
    # Converted to python by spxll 2016
    #
    # This implementation apparently uses the formula given in:
    # https://en.wikipedia.org/wiki/Wigner_D-matrix
    #
    # Specifically, this the formula located here: https://wikimedia.org/api/rest_v1/media/math/render/svg/53fd7befce1972763f7f53f5bcf4dd158c324b55

    #
    from numpy import sqrt,exp,cos,sin,ndarray
    from scipy.special import factorial

    #
    if ( (type(alpha) is ndarray) and (type(beta) is ndarray) and (type(gamma) is ndarray) ):
        alpha,beta,gamma = alpha.astype(float), beta.astype(float), gamma.astype(float)
    else:
        alpha,beta,gamma = float(alpha),float(beta),float(gamma)

    #
    coefficient = sqrt( factorial(ll+mp)*factorial(ll-mp)*factorial(ll+mm)*factorial(ll-mm))*exp( 1j*(mp*alpha+mm*gamma) )

    # NOTE that there may be convention differences where the overall sign of the complex exponential may be negated

    #
    total = 0

    # find smin
    if (mm-mp) >= 0 :
        smin = mm - mp
    else:
        smin = 0

    # find smax
    if (ll+mm) > (ll-mp) :
        smax = ll-mp
    else:
        smax = ll+mm

    #
    if smin <= smax:
        for ss in range(smin,smax+1):
            A = (-1)**(mp-mm+ss)
            A *= cos(beta/2)**(2*ll+mm-mp-2*ss)  *  sin(beta/2)**(mp-mm+2*ss)
            B = factorial(ll+mm-ss) * factorial(ss) * factorial(mp-mm+ss) * factorial(ll-mp-ss)
            total += A/B

    #
    element = coefficient*total
    return element

# Given dictionary of multipoles all with the same l, calculate the roated multipole with (l,mp)
def rotate_wfarrs_at_all_times( l,                          # the l of the new multipole (everything should have the same l)
                                m,                          # the m of the new multipole
                                like_l_multipoles_dict,     # dictionary in the format { (l,m): array([domain_values,+,x]) }
                                euler_alpha_beta_gamma,
                                ref_orientation = None ):             #
    """
    from nrutils
    """

    '''
    Given dictionary of multipoles all with the same l, calculate the roated multipole with (l,mp).
    Key reference -- arxiv:1012:2879
    ~ LL,EZH 2018
    '''

    # Import usefuls
    from numpy import exp, pi, array, ones, sign, complex128
#     from nrutils.manipulate.rotate import wdelement

    #
    alpha,beta,gamma = euler_alpha_beta_gamma

    #
    if not ( ref_orientation is None ) :
        raise ValueError('The use of "ref_orientation" has been depreciated for this function.')

    # Handle the default behavior for the reference orientation
    if ref_orientation is None:
        ref_orientation = ones(3)

    # Apply the desired offecrt for the reference orientation. NOTE that this is primarily useful for BAM run which have an atypical coordinate setup if Jz<0
    gamma *= sign( ref_orientation[-1] )
    alpha *= sign( ref_orientation[-1] )

    # Test to see if the original wfarr is complex and if so set the new wfarr to be complex as well
    wfarr_type = type( like_l_multipoles_dict[list(like_l_multipoles_dict.keys())[0]][:,1][0] )

    #
    # new_ylm = 0
    if wfarr_type == complex128:
        new_plus  = 0 + 0j
        new_cross = 0 + 0j
    else:
        new_plus  = 0
        new_cross = 0
    for lm in like_l_multipoles_dict:
        # See eq A9 of arxiv:1012:2879
        l,mp = lm
        old_wfarr = like_l_multipoles_dict[lm]

        #
        # y_mp = old_wfarr[:,1] + 1j*old_wfarr[:,2]
        # new_ylm += wdelement(l,m,mp,alpha,beta,gamma) * y_mp

        #
        d = wdelement(l,m,mp,alpha,beta,gamma)
        a,b = d.real,d.imag
        #
        p = old_wfarr[:,1]
        c = old_wfarr[:,2]
        #
        new_plus  += a*p - b*c
        new_cross += b*p + a*c

    # Construct the new waveform array
    t = old_wfarr[:,0]

    #
    # ans = array( [ t, new_ylm.real, new_ylm.imag ] ).T
    ans = array( [ t, new_plus, new_cross ] ).T

    # Return the answer
    return ans


# Calculate the emission tensor given a dictionary of multipole data
def calc_Lab_tensor( multipole_dict ):
    """
    from nrutils
    """

    '''
    Given a dictionary of multipole moments (single values or time series)
    determine the emission tensor, <L(aLb)>.
    The input must be a dictionary of the format:
    { (2,2):wf_data22, (2,1):wf_data21, ... (l,m):wf_datalm }
    Key referece: https://arxiv.org/pdf/1304.3176.pdf
    Secondary ref: https://arxiv.org/pdf/1205.2287.pdf
    Lionel London 2017
    '''

    # Import usefuls
    from numpy import sqrt,zeros_like,ndarray,zeros,double

    # Rename multipole_dict for short-hand
    y = multipole_dict

    # Allow user to input real and imag parts separately -- this helps with sanity checks
    if isinstance( y[2,2], dict ):
        #
        if not ( ('real' in y[2,2]) and ('imag' in y[2,2]) ):
            raise ValueError('You\'ve entered a multipole dictionary with separate real and imaginary parts. This must be formatted such that y[2,2]["real"] gives the real part and ...')
        #
        x = {}
        lmlist = y.keys()
        for l,m in lmlist:
            x[l,m]        = y[l,m]['real'] + 1j*y[l,m]['imag']
            x[l,m,'conj'] = x[l,m].conj()
    elif isinstance( y[2,2], (float,int,complex,ndarray) ):
        #
        x = {}
        lmlist = y.keys()
        for l,m in lmlist:
            x[l,m]        = y[l,m]
            x[l,m,'conj'] = y[l,m].conj()
    #
    y = x


    # Check type of dictionary values and pre-allocate output
    if isinstance( y[2,2], (float,int,complex) ):
        L = zeros( (3,3), dtype=complex )
    elif isinstance( y[2,2], ndarray ):
        L = zeros( (3,3,len(y[2,2])), dtype=complex )
    else:
        raise ValueError('Dictionary values of handled type; must be float or array')

    # define lambda function for useful coeffs
    c = lambda l,m: sqrt( l*(l+1) - m*(m+1) ) if abs(m)<=l else 0

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Compute tensor elements (Eqs. A1-A2 of https://arxiv.org/pdf/1304.3176.pdf)
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

    # Pre-allocate elements
    I0,I1,I2,Izz = zeros_like(y[2,2]), zeros_like(y[2,2]), zeros_like(y[2,2]), zeros_like(y[2,2])

    # Sum contributions from input multipoles
    for l,m in lmlist:

        # Eq. A2c
        I0 += 0.5 * ( l*(l+1)-m*m ) * y[l,m] * y[l,m,'conj']

        # Eq. A2b
        I1 += c(l,m) * (m+0.5) * ( y[l,m+1,'conj'] if (l,m+1) in y else 0 ) * y[l,m]

        # Eq. A2a
        I2 += 0.5 * c(l,m) * c(l,m+1) * y[l,m] * ( y[l,m+2,'conj'] if (l,m+2) in y else 0 )

        # Eq. A2d
        Izz += m*m * y[l,m] * y[l,m,'conj']

    # Compute the net power (amplitude squared) of the multipoles
    N = sum( [ y[l,m] * y[l,m,'conj'] for l,m in lmlist ] ).real

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Populate the emission tensor ( Eq. A2e )
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

    # Populate asymmetric elements
    L[0,0] = I0 + I2.real
    L[0,1] = I2.imag
    L[0,2] = I1.real
    L[1,1] = I0 - I2.real
    L[1,2] = I1.imag
    L[2,2] = Izz
    # Populate symmetric elements
    L[1,0] = L[0,1]
    L[2,0] = L[0,2]
    L[2,1] = L[1,2]

    # Normalize
    N[ N==0 ] = min( N[N>0] )
    L = L.real / N

    #
    return L

# Look for point reflections in vector and correct
def reflect_unwrap( vec ):
    """
    from positive.maths
    """
    '''Look for point reflections in vector and correct'''

    #
    from numpy import array,sign,zeros_like

    #
    ans = array(vec)

    #
    for k,v in enumerate(vec):

        #
        if (k>0) and ( (k+1) < len(vec) ):

            #
            l = vec[k-1]
            c = vec[k]
            r = vec[k+1]

            #
            apply_reflection = (sign(l)==sign(r)) and (sign(l)==-sign(c))
            if apply_reflection:

                #
                ans[k] *= -1

    #
    return ans


# Return the min and max limits of an 1D array
def lim(x,dilate=0):
    """
    from positive.maths
    """

    '''
    Return the min and max limits of an 1D array.
    INPUT
    ---
    x,              ndarray
    dilate=0,       fraction of max-min by which to expand or contract output
    RETURN
    ---
    array with [min(x),max(x)]
    '''

    # Import useful bit
    from numpy import array,amin,amax,ndarray,diff

    # ensure is array
    if not isinstance(x,ndarray): x = array(x)

    # Columate input.
    z = x.reshape((x.size,))

    #
    ans = array([min(z),max(z)]) + (0 if len(z)>1 else array([-1e-20,1e-20]))

    #
    if dilate != 0: ans += diff(ans)*dilate*array([-1,1])

    # Return min and max as list
    return ans


# Clone of MATLAB's find function: find all of the elements in a numpy array that satisfy a condition.
def find( bool_vec ):
    """
    from positive.maths
    """

    #
    from numpy import where

    #
    return where(bool_vec)[0]

def spline_diff(t,y,k=3,n=1):
    """
    from positive.maths
    """
    '''
    Wrapper for InterpolatedUnivariateSpline derivative function
    '''

    #
    from numpy import sum
    from scipy.interpolate import InterpolatedUnivariateSpline as spline

    # Calculate the desired number of derivatives
    ans = spline(t,y.real,k=k).derivative(n=n)(t) \
          + ( 1j*spline(t,y.imag,k=k).derivative(n=n)(t) if (sum(abs(y.imag))!=0) else 0 )

    return ans

#
def spline_antidiff(t,y,k=3,n=1):
    """
    from positive.maths
    """
    '''
    Wrapper for InterpolatedUnivariateSpline antiderivative function
    '''

    #
    from scipy.interpolate import InterpolatedUnivariateSpline as spline

    # Calculate the desired number of integrals
    ans = spline(t,y.real,k=k).antiderivative(n=n)(t) + ( 1j*spline(t,y.imag,k=k).antiderivative(n=n)(t) if isinstance(y[0],complex) else 0 )

    # Return the answer
    return ans


# Given a dictionary of multipole data, calculate the Euler angles corresponding to a co-precessing frame
def calc_coprecessing_angles( multipole_dict,       # Dict of multipoles { ... l,m:data_lm ... }
                              domain_vals = None,   # The time or freq series for multipole data
                              ref_orientation = None, # e.g. initial J; used for breaking degeneracies in calculation
                              return_xyz = False,
                              safe_domain_range = None,
                              verbose = None ):
    """
    from nrutils
    """

    '''
    Given a dictionary of multipole data, calculate the Euler angles corresponding to a co-precessing frame
    Key referece: https://arxiv.org/pdf/1304.3176.pdf
    Secondary ref: https://arxiv.org/pdf/1205.2287.pdf
    INPUT
    ---
    multipole_dict,       # dict of multipoles { ... l,m:data_lm ... }
    t,                    # The time series corresponding to multipole data; needed
                            only to calculate gamma; Optional
    verbose,              # Toggle for verbosity
    OUTPUT
    ---
    alpha,beta,gamma euler angles as defined in https://arxiv.org/pdf/1205.2287.pdf
    AUTHOR
    ---
    Lionel London (spxll) 2017
    '''

    # Import usefuls
    from scipy.linalg import eig,norm
    from numpy import arctan2,sin,arcsin,pi,ones,arccos,double,array
    from numpy import unwrap,argmax,cos,array,sqrt,sign,argmin,round

    # Handle optional input
    # if ref_orientation is None: ref_orientation = ones(3)
    if ref_orientation is None: ref_orientation = np.array([0,0,1])

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Enforce that multipole data is array typed with a well defined length
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    y = multipole_dict
    for l,m in y:
        if isinstance( y[l,m], (float,int) ):
            y[l,m] = array( [ y[l,m], ] )
        else:
            if not isinstance(y[l,m],dict):
                # Some input validation
                if domain_vals is None: raise ValueError( 'Since your multipole data is a series, you must also input the related domain_vals (i.e. times or frequencies) array' )
                if len(domain_vals) != len(y[l,m]): raise ValueError('domain_vals array and multipole data not of same length')


    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Calculate the emission tensor corresponding to the input data
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    L = calc_Lab_tensor( multipole_dict )

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Compute the eigenvectors and values of this tensor
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

    # NOTE that members of L have the same length as each y[l,m]; the latter has been
    # forced to always have a length above

    # Initialize idents for angles. NOTE that gamma will be handled below
    alpha,beta = [],[]
    X,Y,Z = [],[],[]

    #
    # reference_z_scale = None
    old_dom_dex = None

    # For all multipole instances
    ref_x,ref_y,ref_z = None,None,None
    flip_z_convention = False
    for k in range( len(L[0,0,:]) ):

        # Select the emission matrix for this instance, k
        _L = L[:,:,k]

        # Compute the eigen vals and vecs for this instance
        vals,vec = eig( _L )

        # Find the dominant direction's index
        dominant_dex = argmax( vals )
        if old_dom_dex is None: old_dom_dex = dominant_dex
        if old_dom_dex != dominant_dex:
            # print dominant_dex
            old_dom_dex = dominant_dex

        # Select the corresponding vector
        dominant_vec = vec[ :, dominant_dex ]

        # There is a z axis degeneracy that we will break here
        # by imposing that the z component is always positive
        # NOTE the following exceptions:
        #  * The optimal emission direction crosses the x-y plane
        #  * Data is processed in a frequency-like domain where f<0 may have z<0

        # if not flip_z_convention:
        #     if sign(dominant_vec[-1]) == -sign(ref_orientation[-1]): dominant_vec *= -1
        # else:
        #     if sign(dominant_vec[-1]) ==  sign(ref_orientation[-1]): dominant_vec *= -1

        # dominant_vec *= sign(domain_vals[k])*sign(ref_orientation[-1])
        # if sign(dominant_vec[-1]) == -sign(ref_orientation[-1]): dominant_vec *= -1

        if not flip_z_convention:
            if sign(dominant_vec[-1]) == -sign(ref_orientation[-1]): dominant_vec *= -1
        else:
            if sign(dominant_vec[-1]) ==  sign(ref_orientation[-1]): dominant_vec *= -1

        # dominant_vec *= sign(domain_vals[k])

        # Extract the components of the dominant eigenvector
        _x,_y,_z = dominant_vec

        # Store reference values if they are None
        if ref_x==None:
            ref_x = _x
            ref_y = _y
            ref_z = _z
        else:
            if (ref_x*_x < 0) and (ref_y*_y < 0):
                _x *= -1
                _y *= -1
                _x *= -1

        # Store unit components for reference in the next iternation
        ref_x = _x
        ref_y = _y
        ref_z = _z

        # Look for and handle trivial cases
        if abs(_x)+abs(_y) < 1e-8 :
            _x = _y = 0

        #
        X.append(_x);Y.append(_y);Z.append(_z)

    # Look for point reflection in X
    X = reflect_unwrap(array(X))
    Y = array(Y)
    Z = array(Z)

    # 3-point vector reflect unwrapping
    # print safe_domain_range
    tol = 0.1
    if safe_domain_range is None: safe_domain_range = lim(abs(domain_vals))
    safe_domain_range = array( safe_domain_range )
    from numpy import arange,mean
    for k in range(len(X))[1:-1]:
        if k>0 and k<(len(domain_vals)-1):

            if (abs(domain_vals[k])>min(abs(safe_domain_range))) and (abs(domain_vals[k])<max(abs(safe_domain_range))):

                left_x_has_reflected = abs(X[k]+X[k-1])<tol*abs(X[k-1])
                left_y_has_reflected = abs(Y[k]+Y[k-1])<tol*abs(X[k-1])

                right_x_has_reflected = abs(X[k]+X[k+1])<tol*abs(X[k])
                right_y_has_reflected = abs(Y[k]+Y[k+1])<tol*abs(X[k])

                x_has_reflected = right_x_has_reflected or left_x_has_reflected
                y_has_reflected = left_y_has_reflected or right_y_has_reflected

                if x_has_reflected and y_has_reflected:

                    # print domain_vals[k]

                    if left_x_has_reflected:
                        X[k:] *=-1
                    if right_x_has_reflected:
                        X[k+1:] *= -1

                    if left_y_has_reflected:
                        Y[k:] *=-1
                    if right_y_has_reflected:
                        Y[k+1:] *= -1

                    Z[k:] *= -1


    # # Enforce that the initial direction of Z is the same as the input reference orientation
    index_ref = find( domain_vals>min(abs(safe_domain_range)) )[0]
    Z_ref = Z[ index_ref ]
    # print 'len(domain_vals) = ',len(domain_vals)
    # print 'index_ref = ',index_ref
    # print 'Z_ref = ',Z_ref
    # print 'ref_orientation = ',ref_orientation
    if Z_ref != 0:
        if sign(Z_ref) != sign( ref_orientation[-1] ):
            warnings.warn("Reference orientation and calculated data inconsistent. We will reflect.")
            Z *= -1
            Y *= -1
            X *= -1

    # Make sure that imag parts are gone
    X = double(X)
    Y = double(Y)
    Z = double(Z)

    #################################################
    # Reflect Y according to nrutils conventions    #
    Y = -Y                                          #
    #################################################

    a = array(ref_orientation)/norm(ref_orientation)
    B = array([X,Y,Z]).T
    b = (B.T/norm(B,axis=1)).T
    xb,yb,zb = b.T
    test_quantity = a[0]*xb+a[1]*yb+a[2]*zb

    mask = (domain_vals>=min(safe_domain_range)) & (domain_vals<=max(safe_domain_range))
    if 1*(test_quantity[mask][0])<0:
        warnings.warn('flipping manually for negative domain')
        X = -X
        Y = -Y
        Z = -Z

    # -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~- #
    #                          Calculate Angles                           #
    # -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~- #

    alpha = arctan2(Y,X)
    beta  = arccos(Z)

    # Make sure that angles are unwrapped
    alpha = unwrap( alpha )
    beta  = unwrap( beta  )

    # Calculate gamma (Eq. A4 of of arxiv:1304.3176)
    if len(alpha) > 1 :
        k = 1
        # NOTE that spline_diff and spline_antidiff live in positive.maths
        gamma = - spline_antidiff( domain_vals, cos(beta) * spline_diff(domain_vals,alpha,k=k), k=k  )
        gamma = unwrap( gamma )
    else:
        # NOTE that this is the same as above, but here we're choosing an integration constant such that the value is zero. Above, no explicit integration constant is chosen.
        gamma = 0

    # Return answer
    if return_xyz == 'all':
        #
        return alpha,beta,gamma,X,Y,Z
    elif return_xyz:
        #
        return X,Y,Z
    else:
        return alpha,beta,gamma

def calc_coprecessing_angles_scri(multipole_dict, domain_vals, RoughDirection=None, RoughDirectionIndex=0):
    from scipy.linalg import eigh
    Lab = calc_Lab_tensor(multipole_dict)
    val, vec = [], []
    for i in range(Lab.shape[2]):
        _val, _vec = eigh(Lab[:,:,i])
        val.append(_val)
        vec.append(_vec)
    val = np.array(val)
    vec = np.array(vec)
    # dpa = eigenvecs[:, :, 2]  # `eigh` always returns eigenvals in *increasing* order
    if RoughDirection is None:
        RoughDirection=np.array([0,0,1])
    else:
        # enforce it to be numpy.ndarray
        RoughDirection = np.array(RoughDirection)
    dpa = vec[:,:,2]
    dpa = _LLDominantEigenvector(dpa, dpa_i=RoughDirection, i_index=RoughDirectionIndex)
    X, Y, Z = dpa.T

    # alpha needed a minus sign for convention reasons...
    alpha = -np.unwrap(np.arctan2(Y,X))
    beta  = np.arccos(Z)
    k = 1
    # NOTE that spline_diff and spline_antidiff live in positive.maths
    gamma = - spline_antidiff( domain_vals, np.cos(beta) * spline_diff(domain_vals,alpha,k=k), k=k  )
    gamma = np.unwrap( gamma )

    return alpha, beta, gamma, X, Y, Z


def _LLDominantEigenvector(dpa, dpa_i, i_index):
    """Taken from https://github.com/moble/scri/blob/master/mode_calculations.py

    Now we find and normalize the dominant principal axis (dpa) at each
    moment, made continuous
    """
    dpa = dpa.copy()
    # Make the initial direction closer to RoughInitialEllDirection than not
    if (
        dpa_i[0] * dpa[i_index, 0]
        + dpa_i[1] * dpa[i_index, 1]
        + dpa_i[2] * dpa[i_index, 2]
    ) < 0.0:
        dpa[i_index, 0] *= -1
        dpa[i_index, 1] *= -1
        dpa[i_index, 2] *= -1
    # Now, go through and make the vectors reasonably continuous.
    d = -1
    LastNorm = np.sqrt(dpa[i_index, 0] ** 2 + dpa[i_index, 1] ** 2 + dpa[i_index, 2] ** 2)
    for i in range(i_index - 1, -1, -1):
        Norm = dpa[i, 0] ** 2 + dpa[i, 1] ** 2 + dpa[i, 2] ** 2
        dNorm = (
            (dpa[i, 0] - dpa[i - d, 0]) ** 2
            + (dpa[i, 1] - dpa[i - d, 1]) ** 2
            + (dpa[i, 2] - dpa[i - d, 2]) ** 2
        )
        if dNorm > Norm:
            dpa[i, 0] *= -1
            dpa[i, 1] *= -1
            dpa[i, 2] *= -1
        # While we're here, let's just normalize that last one
        if LastNorm != 0.0 and LastNorm != 1.0:
            dpa[i - d, 0] /= LastNorm
            dpa[i - d, 1] /= LastNorm
            dpa[i - d, 2] /= LastNorm
        LastNorm = np.sqrt(Norm)
    if LastNorm != 0.0 and LastNorm != 1.0:
        dpa[0, 0] /= LastNorm
        dpa[0, 1] /= LastNorm
        dpa[0, 2] /= LastNorm
    d = 1
    LastNorm = np.sqrt(dpa[i_index, 0] ** 2 + dpa[i_index, 1] ** 2 + dpa[i_index, 2] ** 2)
    for i in range(i_index + 1, dpa.shape[0]):
        Norm = dpa[i, 0] ** 2 + dpa[i, 1] ** 2 + dpa[i, 2] ** 2
        dNorm = (
            (dpa[i, 0] - dpa[i - d, 0]) ** 2
            + (dpa[i, 1] - dpa[i - d, 1]) ** 2
            + (dpa[i, 2] - dpa[i - d, 2]) ** 2
        )
        if dNorm > Norm:
            dpa[i, 0] *= -1
            dpa[i, 1] *= -1
            dpa[i, 2] *= -1
        # While we're here, let's just normalize that last one
        if LastNorm != 0.0 and LastNorm != 1.0:
            dpa[i - d, 0] /= LastNorm
            dpa[i - d, 1] /= LastNorm
            dpa[i - d, 2] /= LastNorm
        LastNorm = np.sqrt(Norm)
    if LastNorm != 0.0 and LastNorm != 1.0:
        dpa[-1, 0] /= LastNorm
        dpa[-1, 1] /= LastNorm
        dpa[-1, 2] /= LastNorm
    return dpa

def convert_to_nrutils_dict(times, hlms):
    """
    convert input times and hlms into a format that nrutils
    based function 'rotate_wfarrs_at_all_times' can read.
    times: numpy array of times
    hlms: dict with keys [(2,2), (2,1), (2,0), ...]
        containing 1d array of complex numbers
    returns:
    hlms_3col: dict with same keys as 'hlms' but now values
        are 3 col arrays of [time, re(hlm), im(hlm)]
    """
    hlms_3col = {}
    for k in hlms.keys():
        hlms_3col[k] = np.array([times, np.real(hlms[k]), np.imag(hlms[k])]).T
    return hlms_3col
