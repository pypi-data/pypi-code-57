#!/usr/bin/env Python3
from .ciddorModel import Observatory
from .refractionModels import refraction
from .dispersionModels import dispersion

'''
@ Author: 		Joost van den Born
@ Contact: 		born@astron.nl
@ Description: 	Some functions for quick testing.
'''


def quick_refractive_index(l, conditions='STANDARD', T=288.15, p=101325, 
							H=0.0, xc=450, lat=0, h=0):
	'''
		Function to quickly calculate the refractive index
		of atmospheric air at reference conditions, given 
		a wavelength l.

		Parameters
		----------
		l 	: float
			Wavelength in microns
		conditions: string
			'STANDARD' or 'CERRO_ARMAZONES', refers
			to the standard atmospheric conditions.
		T 	: float (optional)
			Temperature in Kelvin
		p 	: float (optional)
			Atmospheric pressure in Pa
		H 	: float (optional)
			Relative humidity
		xc 	: float (optional)
			CO2 density in parts per million
		lat : float (optional)
			Latitude of the observer in degrees
		h 	: float (optional)
			Altitude of the observer in meters
	
		Returns
		-------
		n 	: 	float
			Refractive index for the given conditions.
	'''
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		p   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		
	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		p   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l
	n 	= at.n_tph(l=l, T=T, p=p, RH=H, xc=xc)
	return n


def quick_refraction(l, z, conditions='STANDARD', T=288.15, p=101325, 
							H=0.0, xc=450, lat=0, h=0):
	'''
		Function to quickly calculate the refraction
		of atmospheric air at reference conditions, 
		given a wavelength l.

		Parameters
		----------
		l  	: 	float 
			Wavelength in microns
		z  	: 	float 
			Zenith angle of the observation
		conditions 	: string
			'STANDARD' or 'CERRO_ARMAZONES', refers
			to the standard atmospheric conditions.
		T  	: 	float (optional)
			Temperature in Kelvin
		p  	: 	float (optional)
			Atmospheric pressure in Pa
		H  	: 	float (optional)
			Relative humidity
		xc  : 	float (optional)
			CO2 density in parts per million
		lat : 	float (optional)
			Latitude of the observer in degrees
		h  	: 	float (optional)
			Altitude of the observer in meters
	
		Returns
		-------
		R 	: 	float
			Refraction in degrees
	'''
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		p   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		
	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		p   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l
	n 	= at.n_tph(l=l, T=T, p=p, RH=H, xc=xc)

	# Density of the atmosphere (following CIPM-81/91 equations)
	rho = at.rho(p=p, T=T, RH=H, xc=xc)

	# Initializing refraction model and setting the reduced height
	ref = refraction(lat, h)
	ref.setReducedHeight(p, rho)
	return ref.cassini(n, z)


def quick_dispersion(l1, l2, z, conditions='STANDARD', T=288.15, 
						p=101325, H=0.0, xc=450, lat=0, h=0):
	'''
		Function to quickly calculate the dispersion
		of atmospheric air at reference conditions, 
		given a wavelength l.

		Parameters
		----------
		l1 	: 	float
			Shortest wavelength of interest in micron.
		l2 	: 	float
			Longest wavelength of interest in micron.
		z 	: 	float
			Zenith angle of the observation
		conditions 	: string
			'STANDARD' or 'CERRO_ARMAZONES', refers
			to the standard atmospheric conditions.
		T 	: 	float (optional)
			Temperature in Kelvin
		p 	: 	float (optional)
			Atmospheric pressure in Pa
		H 	: 	float (optional)
			Relative humidity
		xc 	: 	float (optional)
			CO2 density in parts per million
		lat : 	float (optional)
			Latitude of the observer in degrees
		h 	: 	float (optional)
			Altitude of the observer in meters
	
		Returns
		-------
		dR 	: float
		 	Atmospheric dispersion in degrees
	'''
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		p   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		
	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		p   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l1 and l2
	n1 	= at.n_tph(l=l1, T=T, p=p, RH=H, xc=xc)
	n2 	= at.n_tph(l=l2, T=T, p=p, RH=H, xc=xc)

	# Density of the atmosphere (following CIPM-81/91 equations)
	rho = at.rho(p=p, T=T, RH=H, xc=xc)

	# Initializing refraction model and setting the reduced height
	disp = dispersion(lat, h)
	disp.setReducedHeight(p, rho)
	return disp.cassini(n1, n2, z)