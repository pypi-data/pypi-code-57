# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	'''
	/////////////////////////////////////////////////////////////////////////
	//
	// \xa9 University of Southampton IT Innovation, 2014
	//
	// Copyright in this software belongs to IT Innovation Centre of
	// Gamma House, Enterprise Road, Southampton SO16 7NS, UK.
	//
	// This software may not be used, sold, licensed, transferred, copied
	// or reproduced in whole or in part in any manner or form or in or
	// on any media by any person other than in accordance with the terms
	// of the Licence Agreement supplied with the software, or otherwise
	// without the prior written consent of the copyright owners.
	//
	// This software is distributed WITHOUT ANY WARRANTY, without even the
	// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
	// PURPOSE, except where stated in the Licence Agreement supplied with
	// the software.
	//
	//	Created By :	Stuart E. Middleton
	//	Created Date :	2014/03/04
	//	Created for Project:	REVEAL
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies: None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

Time utility functions
"""

import sys,traceback, copy, logging, datetime

#
# A UTC timezone class since all PCAP timestamps are UTC
# e.g.
#   utc = time_helper.UTC()
#   dateUTC = dateRelativeToMakeUTC.replace( tzinfo=utc )
#   strISODate = dateUTC.isoformat()
#
class UTC( datetime.tzinfo ) :
	def utcoffset(self, dt) :
		return datetime.timedelta(0)
	def tzname(self, dt) :
		return "UTC"
	def dst(self, dt) :
		return datetime.timedelta(0)

def parse_iso_datetime( date_text = None ) :
	"""
	Parse ISO date string to a python datetime object with a UTC timezone

	| note: does not support microsconds such as '2014-02-01T01:02:03.123456+01:30'

	:param kwargs: variable argument to override any default config values

	:return: configuration settings to be used by all common_parse_lib functions
	:rtype: dict
	"""

	if not isinstance( date_text, str ) :
		raise Exception( 'invalid date_text' )

	try :
		if len(date_text) < 25 :
			raise Exception( 'date string too short (incorrect format? expected yyyy-mm-ddThh:mm:ss+zz:zz)' )
		if len(date_text) > 25 :
			raise Exception( 'date string too long (incorrect format? expected yyyy-mm-ddThh:mm:ss+zz:zz)' )

		dateResult = datetime.datetime.strptime( date_text[:-6], '%Y-%m-%dT%H:%M:%S' )

		nHour = int( date_text[-6:-3] )
		nMinute = int( date_text[-2:] )
		if nHour == None or nMinute == None :
			raise Exception( 'GMT offset failed to parse' )
		if nHour < 0 :
			nMinute = -1 * nMinute
		dateResult = dateResult + datetime.timedelta( hours=nHour, minutes=nMinute )

		utc = UTC()
		dateResult = dateResult.replace( tzinfo=utc )

		return dateResult
	except :
		raise Exception( 'ISO datetime parse failed for ' + repr(date_text) + ' : ' + str(sys.exc_info()[1]) )

# e.g.
#   utc = time_helper.UTC()
#   dateRelative = datetime.datetime.now()
#   dateUTC = dateRelative.replace( tzinfo=utc )
#   print time_helper.format_iso_datetime( dateUTC )
#
def format_iso_datetime( date_with_timezone = None ) :
	"""
	Format date object (with a timezone) into an ISO formatted string yyyy-mm-ddThh:mm:ss+zz:zz

	| note: any microseconds will be truncated in serialized output

	:param kwargs: variable argument to override any default config values

	:return: configuration settings to be used by all common_parse_lib functions
	:rtype: dict
	"""

	if not isinstance( date_with_timezone, datetime.datetime ) :
		raise Exception( 'invalid date_with_timezone' )

	try :
		if date_with_timezone.tzinfo == None :
			raise Exception( 'null date timezone (relative dates cannot be ISO serialized with a GMT offset)' )

		dateTruncated = date_with_timezone.replace( microsecond=0 )

		return dateTruncated.isoformat()
	except :
		raise Exception( 'ISO datetime format failed for ' + repr(date_with_timezone) + ' : ' + str(sys.exc_info()[1]) )
	
	
	
# e.g.
#	dateConverted = convert_datetime_tz_iso( datetime.now() )
#
def convert_datetime_tz_iso( date_without_timezone = None ) :
	"""
	Convert standard datetime.now object (e.g. 2014-03-06 14:13:27.733000) to ISO formatted (yyyy-mm-ddThh:mm:ss+zz:zz) and timezone aware (UTC timezone) datetime object

	| note: any microseconds will be truncated in serialized output

	:param kwargs: variable argument to override any default config values

	:return: configuration settings to be used by all common_parse_lib functions
	:rtype: dict
	"""

	try :
		utc = UTC()
		dateResult = date_without_timezone.replace( tzinfo=utc )
		dateResult = format_iso_datetime( dateResult )
		
		return parse_iso_datetime( dateResult )
	except :
		raise Exception( 'Convert to ISO formated and timezone aware datetime object failed for ' + repr(date_without_timezone) + ' : ' + str(sys.exc_info()[1]) )
