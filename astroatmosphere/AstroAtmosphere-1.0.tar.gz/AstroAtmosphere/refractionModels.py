#!/usr/bin/env Python3
import numpy as np
from scipy import integrate
import os
from .ciddorModel import Observatory

'''
@ Author:		Joost van den Born 
@ Contact:		born@astron.nl
@ Description:	This script offers a complete model of the atmospheric refraction
				and dispersion. It uses the Ciddor1996 paper to calculate the 
				index of refraction for a wide range of conditions, with corresponding
				error propagation if needed.
				The actual refraction is calculated by any of the following models:
				- Plane parallel atmosphere
				- Cassini spherical homogeneous atmosphere
				- Other methods described in Corbard et al., 2019.
'''

class refraction(Observatory):
	'''
		Class that sets the observer location.
		These location attributes are then used to calculate the 
		appropriate atmospheric refraction.

		See also:
		Observatory()
		dispersion()
		...

		Attributes
		-----------
		lat : 	float
			Latitude of the observer in degrees
		h 	: 	float
			Altitude above mean sea level of the observer in meters
		Other Observatory() attributes

		Methods
		-------
		setReducedHeight(p, rho)
			Sets the reduced atmospheric height.
		planeParallel(n1, n2, zenith)
			Returns the atmospheric refraction assuming a plane parallel
			atmosphere
		cassini(n1, n2, zenith, reduced_height=None)
			Returns the atmospheric refraction asusming Cassini's homegeneous
			atmosphere model
		tan5(n1, n2, zenith, reduced_height=None)
			Returns the atmospheric refraction following Oriani's theorem,
			including a fifth order term in the expansion.
		oriani(n1, n2, zenith, reduced_height=None)
			Returns the atmospheric refraction following the classic version
			of Oriani's theorem.
		corbard(n1, n2, zenith, reduced_height=None)
			Returns the atmospheric refraction following the method described 
			in Corbard et al., 2019.
		refractionIntegral(n1, n2, z0, R0=None, useStandardAtmosphere=True, heightData=None, rhoData=None)
			Returns the atmospheric refraction following the refraction integral.
		psi(x)
			Submethod for corbard()
		set_rc()
			Sets the local radius of curvature of the Earth at the observer.
		set_H(p, rho)
			Sets the reduced height for the conditions at the observer, assuming
			an adiabatic atmosphere.
		H_isotherm(T)
			Sets the reduced height for the conditions at the observer, assuming
			an isothermal atmosphere.
		cassiniError(z, l1, l2, T, p, RH, xc, dl1=0, dl2=0, dT=0.2, dP=20, 
					dRH=0.02, dCO2=20, dz=0, lat=None, h=None)
			Returns the uncertainty in the atmospheric refraction, assuming 
			Cassini's homegeneous atmosphere model and the given parameters.		
		Other Observatory() methods
	'''
	def __init__(self, lat, h):
		Observatory.__init__(self)
		self.h  	= h 					# height above sea level in meters
		self.lat 	= lat					# Latitude of the observer in degrees
		self.rc 	= self.set_rc() * 1000	# Radius of curvature of the earth at the observer
		# self.H2 	= self.H_isotherm(T) 	# Reduced height of isotherm atmosphere

	def setReducedHeight(self, p, rho):
		'''
			Sets the reduced atmospheric height.

			Parameters
			----------
			p 	: float
				Atmospheric pressure in Pascal
			rho : float
				Density of the atmospheric air at the observer
		'''
		self.H  	= self.set_H(p, rho) 		# Reduced height of the atmosphere assuming ideal gas law


	def planeParallel(self, n1, zenith):
		'''
			Refraction based on a flat atmosphere, easily derived from Snell's law.

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			zenith : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.

			Returns
			-------
			R : float
				Atmospheric refraction in degrees
		'''
		_R = np.arcsin(n * np.sin( np.deg2rad(zenith) )) - np.deg2rad(zenith)
		return np.degrees(_R)



	def cassini(self, n1, zenith, reduced_height=None):
		'''
			Refraction of spherical atmosphere, derived from geometry using Sine law

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			zenith : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.
			reduced_height : float (optional)
				Reduced height of the atmosphere. Default value is calculated
				from the object attributes.

			Returns
			-------
			R : float
				Atmospheric refraction in degrees
		'''
		if reduced_height:
			H = reduced_height
		else:
			H = self.H
		
		_R1 = np.arcsin(n1 * self.rc * np.sin(np.deg2rad(zenith)) / (self.rc + H)) - np.arcsin(self.rc * np.sin(np.deg2rad(zenith)) / (self.rc + H) )
		return np.degrees(_R1)



	def tan5(self, n1, zenith, reduced_height=None):
		'''
			Same as oriani's theorem, but including a higher order term.
			Found in Corbard et al., 2019.

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			zenith : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.
			reduced_height : float (optional)
				Reduced height of the atmosphere. Default value is calculated
				from the object attributes.

			Returns
			-------
			R : float
				Atmospheric refraction in degrees
		'''
		if reduced_height:
			H = reduced_height
		else:
			H = self.H
		
		_a = n1 - 1
		_b = H / self.rc
		_R = _a * (1 - _b) * np.tan( np.deg2rad(zenith) )  - _a * (_b - _a/2) * np.tan( np.deg2rad(zenith) )**3 + 3 * _a * (_b - _a/2)**2 * np.tan( np.deg2rad(zenith) )**5
		return np.degrees(_R)



	def oriani(self, n1, zenith, reduced_height=None):
		'''
			Classic refraction formula with two tan(z) terms. This does not 
			assume any information about the structure of the atmosphere. 
			Found with Oriani's theorem.

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			zenith : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.
			reduced_height : float (optional)
				Reduced height of the atmosphere. Default value is calculated
				from the object attributes.

			Returns
			-------
			R : float
				Atmospheric refraction in degrees
		'''
		if reduced_height:
			H = reduced_height
		else:
			H = self.H

		_a = n1 - 1
		_b = H / self.rc
		_R = _a * (1 - _b) * np.tan( np.deg2rad(zenith) ) - _a * (_b - _a/2) * np.tan( np.deg2rad(zenith) )**3
		return np.degrees(_R)



	def corbard(self, n1, zenith, reduced_height=None):
		'''
			Corbard et al., 2019, mention an additional formula based on the error function.
			Oriani's theorem can be derived from this equation by 'keeping only the three first
			terms of its asymptotic expansion'.

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			zenith : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.
			reduced_height : float (optional)
				Reduced height of the atmosphere. Default value is calculated
				from the object attributes.

			Returns
			-------
			R : float
				Atmospheric refraction in degrees
		'''
		if reduced_height:
			H = reduced_height
		else:
			H = self.H

		_a = n1 - 1
		_b = H / self.rc
		_R = _a * ( (2 - _a) / (np.sqrt( 2*_b - _a )) ) * np.sin( np.deg2rad(zenith) ) * self.psi( (np.cos(np.deg2rad(zenith))) / np.sqrt(2*_b - _a) )
		return np.degrees(_R)



	def refractionIntegral(self, n1, z0, R0=None, useStandardAtmosphere=True, heightData=None, rhoData=None):
		'''
			Using data that gives temperature, pressure and density as a 
			function of height, the gladstone-dale relation is invoked to
			calculate the path of a light ray along the atmosphere. 
			This is allows us to also include atmospheric activity in 
			different atmosphere layers.
			Recommended use with the US Standard Atmosphere from 1976.
			USSA1976 data generated from code supplied by http://www.pdas.com/atmos.html
			The method described in eq. 3 in Auer & Standish (2000) is used for the 
			calculation.

			Parameters
			----------
			n1 : float
				Refractive index at the wavelength of interest
			z0 : float
				Angle of observation in degrees.
				zenith = 0 means the observation is directly overhead.
			R0 : float (optional)
				Local radius of curvature of the Earth in km.
			useStandardAtmosphere : bool
				Flag to use the included USSA1976 data
			heightData : 1D Array
				If "useStandardAtmosphere" is False, the function will ask
				for alternative atmospheric data to integrate over. This
				gives the altitudinal points
			rhoData : 1D Array
				If useStandardAtmosphere is False, the function will ask
				for alternative atmospheric data to integrate over. This
				gives the atmospheric density at the points defined by 
				"heightData".

			Returns
			-------
			R : float
				Atmospheric refraction in degrees

		'''
		if not R0:
			R0 = self.rc
		if useStandardAtmosphere:
			_datafileLocation = os.path.join(os.path.dirname(__file__), 'data/1976USSA.txt')
			_h, _, _, _, _Temp, _Press, _Dens,_,_,_ = np.genfromtxt(_datafileLocation, unpack=True, skip_header=6)
		else:
			_Dens = rhoData
			_h 	  = heightData

		z0 						= np.deg2rad(z0)
		_Dens 	= np.asarray(_Dens)
		_h 	 	= np.asarray(_h) 
		_R 		= R0 + _h * 1000
		
		# Gladstone-Dale relation between refractive index and density
		_n_h = 1 + (n0 - 1) / _Dens[0] * _Dens 

		# Calculation of the zenith angle for given height and refractive index, from the refractive invariant
		_z 		= np.arcsin( (n0 * R0) / (_n_h * _R) * np.sin(z0) )
		
		# Calculation of log space derivative of n and r
		_lnn = np.log(_n_h)
		_lnr = np.log(_R)
		_dlnn = np.asarray([_lnn[i+1] - _lnn[i] for i in range(len(_lnn)-1)])
		_dlnr = np.asarray([_lnr[i+1] - _lnr[i] for i in range(len(_lnr)-1)])
		_dz   = np.asarray([(_z[i] - _z[i+1]) for i in range(len(_z)-1)])

		# Calculation of the integrand in eq. 3 in Auer & Standish
		_Integrand = -1*(_dlnn/_dlnr) / (1 + _dlnn/_dlnr) * _dz


		return np.degrees(np.sum(_Integrand))



	def psi(self, x):
		'''
			Submethod for corbard(). Described explicitly in Corbard et al.,2019.

			Parameters
			----------
			x 	: 	float
				Input of the function

			Returns
			-------
			y 	: 	float
				Output of the function
		'''
		_f   = lambda a: np.exp(-a**2)
		_int = integrate.quad(_f, x, np.inf)
		return np.exp(x**2) * _int[0]



	def set_rc(self):
		'''
			Returns the radius of the curvature at the observer in km,
			taking into account the latitude of the observer and the corresponding
			ellipsoidality of the earth.

			Returns
			-------
			rc 	: float
				Local radius of curvature of the Earth in kilometers.
		'''
		_A   = 6378.137 # km
		_B   = 6356.752 # km
		_phi = np.deg2rad(self.lat)
		
		_rc0 = (_A*_B)**2 / (_A**2 * np.cos(_phi)**2 + _B**2 * np.sin(_phi)**2)**(3/2)
		return _rc0 + self.h/1000



	def set_H(self, p, rho):
		'''
			Calculates the reduced height of the atmosphere, assuming ideal gas law.

			Parameters
			----------
			p 	: float
				Atmospheric pressure in Pascal
			rho : float
				Density of the atmospheric air at the observer

			Returns
			-------
			H 	: float
				Reduced height of the atmosphere in meters
		'''
		_phi = np.deg2rad(self.lat)
		_c1 = 5.2790414e-3
		_c2 = 2.32718e-5
		_c3 = 1.262e-7
		_c4 = 7e-10
		_g0 = 9.780327 # m/s^2
		_g0_local = _g0 * (1 + _c1 * np.sin(_phi)**2 + _c2 * np.sin(_phi)**4 + _c3 * np.sin(_phi)**6 + _c4 * np.sin(_phi)**8)
		_g = _g0_local - (3.0877e-6 - 4.3e-9 * np.sin(_phi)**2) * self.h + 7.2e-13 * self.h**2
		return p / (rho * _g)

	def H_isotherm(self, T):
		'''
			Calculates the reduced height of the atmosphere, 
			assuming an isotherm distribution.

			Parameters
			----------
			T 	: float
				Atmospheric temperature in Kelvin

			Returns
			-------
			H 	: float
				Reduced height of the atmosphere in meters
		'''
		_kb = 1.38064852e-23 # kg m2 s-2 K-1
		_m  = 4.809651698e-26 # kg (weight per molecule of air, assuming dry air)

		_phi = np.deg2rad(self.lat)
		_c1 = 5.2790414e-3
		_c2 = 2.32718e-5
		_c3 = 1.262e-7
		_c4 = 7e-10
		_g0 = 9.780327 # m/s^2
		_g0_local = _g0 * (1 + _c1 * np.sin(_phi)**2 + _c2 * np.sin(_phi)**4 + _c3 * np.sin(_phi)**6 + _c4 * np.sin(_phi)**8)

		return (_kb*T) / (_m * _g0_local)

	def cassiniError(self, n, dn, zenith, dz=0, reduced_height=None):
		'''
		Calculates the uncertainty in the refraction angle in degrees.
		See Observatory().n_tph() and Observatory().dn_tph() on how to
		calculate the refractive index and it's uncertainty.

		Parameters
		----------
		n 	: 	float
			Refractive index of air
		dn 	: 	float
			Uncertainty in the refractive index of air
		zenith : float
			Angle of observation in degrees.
			zenith = 0 means the observation is directly overhead.
		dz  : 	float (optional)
			Uncertainty in the zenith angle, in degrees.
		reduced_height : float (optional)
			Reduced height of the atmosphere. Default value is calculated
			from the object attributes.

		Returns
		-------
		dR 	: float
			Uncertainty in the atmospheric refraction in degrees.
		'''
		if reduced_height:
			_H = reduced_height
		else:
			_H = self.H
		_zenith = np.deg2rad(zenith)
		_dz = np.deg2rad(dz)
		_R = self.rc
		_dRdn = (_R * np.sin(_zenith)) / ((_R + _H) * np.sqrt(1 - ((n**2 * _R**2 * np.sin(_zenith)**2)/(_R + _H)**2)))

		_dRdz = (_R * np.cos(_zenith)) / (_R + _H) * ( n / np.sqrt(1-(n**2 * _R**2 * np.sin(_zenith)**2)/(_R + _H)**2) - 1 / np.sqrt(1-(_R**2 * np.sin(_zenith)**2)/(_R + _H)**2) )

		_dR = np.sqrt( (_dRdn * dn)**2 + (_dRdz * _dz)**2)

		return np.degrees(_dR)
