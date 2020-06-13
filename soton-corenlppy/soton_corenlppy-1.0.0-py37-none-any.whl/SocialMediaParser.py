# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	/////////////////////////////////////////////////////////////////////////
	//
	// (c) Copyright University of Southampton IT Innovation, 2016
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
	// Created By : Vadims Krivcovs
	// Created Date : 2014/07/16
	// Created for Project: REVEAL
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies: None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

Social media response JSON parser class
"""

import sys, json, datetime, time, logging, os, codecs
# urllib.request, urllib.parse, urllib.error, 
#import soton_corenlppy.time_helper
import soton_corenlppy

#
# Social media json object handler helper class
#
class SocialMediaParser( object ) :
	#
	# constructor
	# logger - reference to the logger instance (default None)
	# Exception: thrown if logger setup fails
	#
	def __init__( self, logger = None ) :
		# setup logger
		if logger == None :
			self.logger = logging.getLogger()
		else :
			self.logger = logger
	
	
	#
	# parse social media object and return parsed(based on social media type) timestamp datetime object from it (e.g. ISO 8601 formatted UTC timestamp)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: return ISO 8601 formatted UTC datetime object (format: yyyy-mm-ddThh:mm:ss+zz:zz) (datetime)
	# e.g. 
	#   2014-07-16T16:00:00+00:00
	# Exception: thrown if social media json object (dict or string) will be None, empty or invalid (not instance of dict or string)
	#
	def get_timestamp( self, objSocialMediaResponse, strSocialMediaType = None ) :
		# store json object variable that will be used to extract social media timestamp value
		jsonObject = None

		# store ISO 8601 formatted UTC timestamp variable
		dateTimeUTC = None

		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse

		# double check if the jsonObject is none or empty
		if jsonObject == None or len( jsonObject ) == 0 :
			raise Exception( 'json object can not be none or empty' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )

		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )

		# check if json object is twitter tweet and try to get timestamp value from it
		if strSocialMediaType == 'twitter' :
			# handle twitter time-stamps
			if 'created_at' in jsonObject :
				strTimestamp = jsonObject[ 'created_at' ]
				if strTimestamp[-5] != ' ' :
					# parse the twitter date string (note %z is not supported so parse offset the hard way) into a datetime object
					nOffsetHours = int(strTimestamp[-5:-2])
					nOffsetMinutes = int(strTimestamp[-2:])
					strDateLocal = strTimestamp[:-6]
					ddate = datetime.datetime.strptime( strDateLocal, '%a, %d %b %Y %H:%M:%S' )
				else :
					# parse the twitter date string (note %z is not supported so parse offset the hard way) into a datetime object
					nOffsetHours = int(strTimestamp[-10:-7])
					nOffsetMinutes = int(strTimestamp[-7:-5])
					strDateLocal = strTimestamp[:-11] +  strTimestamp[-5:]
					ddate = datetime.datetime.strptime( strDateLocal, '%a %b %d %H:%M:%S %Y' )
				utc = soton_corenlppy.time_helper.UTC()
				dateTimeUTC = ( ddate - datetime.timedelta( minutes=nOffsetMinutes, hours=nOffsetHours ) ).replace( tzinfo=utc )
			else :
				self.logger.debug( 'tweet timestamp (e.g. created_at) was not found in (' + repr( jsonObject ) + ')' )

		# check if json object is youtube item and try to get timestamp value from it
		# note: youtube timestamp is RFC 3339 (e.g. 1970-01-01T00:00:00Z)
		elif strSocialMediaType == 'youtube' :
			# handle youtube timestamps (e.g. 2014-03-12T22:12:02.000Z)
			if 'publishedAt' in jsonObject[ 'snippet' ] :
				strTimestamp = jsonObject[ 'snippet' ][ 'publishedAt' ]
				
				# check if the timestamp values is UTC ('Z' should be specified in the end of the timestamp string)
				if strTimestamp[-1:] == 'Z' :
					strTimestampNoTimeZone = strTimestamp[:-1]

					# convert time
					# note: check if microseconds were specified in the timestamp 
					if strTimestampNoTimeZone[19:20] == '.' and len( strTimestampNoTimeZone[20:] ) != 0 :
						# parse the timestamp value including microseconds, e.g. 2014-03-12T22:12:02.123
						# note: if microseconds will be equal to 0 (e.g. .000) then they will be automatically removed
						# by the parser
						dateResult = datetime.datetime.strptime( strTimestampNoTimeZone, '%Y-%m-%dT%H:%M:%S.%f' )

					# parse the RFC 3339 timestamp value without microseconds
					else :
						dateResult = datetime.datetime.strptime( strTimestampNoTimeZone, '%Y-%m-%dT%H:%M:%S' )

					# since its is a UTC timestamp add UTC timezone object to the parsed datetime obhect
					utc = soton_corenlppy.time_helper.UTC()
					dateTimeUTC = dateResult.replace( tzinfo=utc )
			else :
				self.logger.debug( 'youtube item timestamp (e.g. publishedAt) was not found in (' + repr( jsonObject ) + ')' )
				
		# check if json object is instagram media item and try to get timestamp value from it
		# note: instagram timestamp is unix timestamp (note: unix timestamp is created by using UTC timezone)
		elif strSocialMediaType == 'instagram' :
			if 'created_time' in jsonObject :
				strUnixTimestamp = jsonObject[ 'created_time' ]

				# convert unix timestamp to date string representation (e.g. format %Y-%m-%d %H:%M:%S)
				strTimeConverted = datetime.datetime.fromtimestamp( int( strUnixTimestamp ) ).strftime('%Y-%m-%d %H:%M:%S' )
				
				# create a datetime object from the above string
				ddate = datetime.datetime.strptime( strTimeConverted, '%Y-%m-%d %H:%M:%S' )
				
				# create utc timezone aware date
				dateTimeUTC = soton_corenlppy.time_helper.convert_datetime_tz_iso( ddate )
			else :
				self.logger.debug( 'instagram media timestamp (e.g. created_time) was not found in (' + repr( jsonObject ) + ')' )

		# check if json object is foursquare venue 
		# note: there is no timestamps in foursquare venue response json therefore additional timestamp element(itinno:timestamp) will be added to the foursquare 
		# json result during the crawler process (e.g. foursquare venue search)
		# e.g.
		#   "itinno:timestamp" : " 2014-07-16T16:35:38+00:00" 
		elif strSocialMediaType == 'foursquare' :
			if 'itinno:timestamp' in jsonObject :
				strTimestamp = jsonObject[ 'itinno:timestamp' ]

				# parse datetime and create datetime object
				dateTimeUTC = soton_corenlppy.time_helper.parse_iso_datetime( strTimestamp )
			else :
				self.logger.debug( 'foursquare venue media timestamp (e.g. itinno:timestamp) was not found in (' + repr( jsonObject ) + ')' )

		# check if facebook json item
		elif strSocialMediaType == 'facebook' :
			if 'created_time' in jsonObject :
				strTimestamp = jsonObject[ 'created_time' ]

				# facebook timestamp is in the format of 2015-11-09T22:00:00+0000 and it needs parsing in order to be used with time_helper library
				# i.e. format is with column with a colon delimeter e.g. from +0000 create +00:00
				strTimestamp = strTimestamp[:22] + ':' +  strTimestamp[22:]

				# parse datetime and create datetime object
				dateTimeUTC = soton_corenlppy.time_helper.parse_iso_datetime( strTimestamp )

		# if social media will be unknown then return None
		else :
			dateTimeUTC = None

		# return datetime object
		return dateTimeUTC 
	
	
	#
	# parse social media object and return its author (based on social media type)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: author name with social media type prefix (str)
	# e.g. 
	#   author in twitter = '@screen name' 
	#   author in youtube = 'yt:channelId'
	#   author in instagram = 'in:username'
	#   author in facebook = 'fb:user name'
	#   foursquare = None (there is no author in foursquare venue)
	#
	def get_author( self, objSocialMediaResponse, strSocialMediaType = None ) :
		# store json object variable that will be used to extract social media author
		jsonObject = None

		# store author id variable (defaulted to None, NOT '' in order to match other function returns in this class)
		strAuthorId = None

		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse

		# double check if the jsonObject is none or empty
		if jsonObject == None or len( jsonObject ) == 0 :
			raise Exception( 'json object can not be none or empty' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )

		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )

		# check if json object is twitter tweet and try to get author id from it (e.g. screen_name)
		if strSocialMediaType == 'twitter' :
			# handle twitter screen name detection
			if 'user' in jsonObject :
				dictUser = jsonObject['user']

				# check the screen name
				if 'screen_name' in dictUser :
					strAuthorId = '@' + dictUser['screen_name']
				else :
					self.logger.debug( 'tweet user name (e.g. screen_name) was not found in (' + repr( jsonObject ) + ')' )
			else :
				self.logger.debug( 'tweet user (e.g. user) was not found in (' + repr( jsonObject ) + ')' )

		# check if json object is youtube item and try to get author id from it (e.g. channelId)
		elif strSocialMediaType == 'youtube' :
			# check the channelId
			if 'snippet' in jsonObject :
				dictSnippet = jsonObject['snippet']

				if 'channelId' in dictSnippet :
					strAuthorId = 'yt:' + dictSnippet['channelId']
				else :
					self.logger.debug( 'youtube item channelId (e.g. channelId) was not found in (' + repr( jsonObject ) + ')' )
			else :
				self.logger.debug( 'youtube item snippet (e.g. snippet) was not found in (' + repr( jsonObject ) + ')' )

		# check if json object is instagram media item and try to get author id from it (e.g. username)
		elif strSocialMediaType == 'instagram' :
			if 'user' in jsonObject :
				dictUser = jsonObject['user']

				# check the screen name
				if 'username' in dictUser :
					strAuthorId = 'in:' + dictUser['username']
				else :
					self.logger.debug( 'instagram media username (e.g. username) was not found in (' + repr( jsonObject ) + ')' )
			else :
				self.logger.debug( 'instagram media user (e.g. user) was not found in (' + repr( jsonObject ) + ')' )	

		# if facebook
		elif strSocialMediaType == 'facebook' :
			
			if 'from' in jsonObject :
				if 'name' in jsonObject['from'] :
					strAuthorId = 'fb:' + jsonObject['from']['name']

		# check if json object is foursquare venue 
		# note: there is not timestamps in foursquare venue response json, thefore None will be returned
		elif strSocialMediaType == 'foursquare' :
			strAuthorId = None
		# if social media will be unknown then return None
		else :
			strAuthorId = None

		# return author id
		return strAuthorId 

	#
	# parse social media object source URI
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: URI string
	#
	def get_source_uri( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		strURI = ''
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			strUserScreenName = ''
			if 'user' in jsonObject :
				dictUser = jsonObject['user']
				if 'screen_name' in dictUser :
					strUserScreenName = dictUser['screen_name']

			if len(strUserScreenName) > 0 :
				strURI = 'https://twitter.com/' + strUserScreenName + '/status/' + jsonObject['id_str']

		elif strSocialMediaType == 'youtube' :

			strItemID = ''
			if 'id' in jsonObject :
				if 'videoId' in jsonObject['id'] :
					strItemID = jsonObject['id']['videoId']

			if len(strItemID) > 0 :
				strURI = 'https://youtube.com/watch?v=' + strItemID

		elif strSocialMediaType == 'instagram' :

			if 'link' in jsonObject :
				strURI = jsonObject['link']


		# TODO: check this one
		elif strSocialMediaType == 'foursquare' :

			# get venue id
			strVenueID = ''
			if 'id' in jsonObject :
				strVenueID = jsonObject['id']
			
			# get title
			strTitle = ''
			if 'name' in jsonObject :
				strTitle = jsonObject['name']
			
			# get source uri
			# note: part of the source uri need to be costructed based on venue name
			# e.g.
			# if venue name is 'the super pub', then part of the source uri should be 'the-super-pub' (https://foursquare.com/v/the-super-pub/<id of the super pub>)
			strSourceUriVenueName = ''
			if strTitle != None and len( strTitle ) > 0 :
				if ' ' in strTitle :
					listSourceNameParts = strTitle.split( ' ' )
					for strSourceNamePart in listSourceNameParts :
						strSourceUriVenueName = strSourceUriVenueName + strSourceNamePart + '-'
					if strSourceUriVenueName[-1:] == '-' :
						strSourceUriVenueName = strSourceUriVenueName[:-1]
				else :
					strSourceUriVenueName = strTitle
				strURI = 'https://foursquare.com/v/' + strSourceUriVenueName + '/' + strVenueID

		elif strSocialMediaType == 'facebook' :
			if 'permalink_url' in jsonObject :
				strURI = jsonObject['permalink_url']

		return strURI

	#
	# parse social media object author URI
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: URI string
	#
	def get_author_uri( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		strURI = ''
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			strUserScreenName = ''
			if 'user' in jsonObject :
				dictUser = jsonObject['user']
				if 'screen_name' in dictUser :
					strUserScreenName = dictUser['screen_name']

			if len(strUserScreenName) > 0 :
				strURI = 'https://twitter.com/' + strUserScreenName

		elif strSocialMediaType == 'youtube' :

			strChannelID = ''
			dictSnippet = jsonObject['snippet']
			if 'channelId' in dictSnippet :
				strChannelID = dictSnippet['channelId']

			if len(strChannelID) > 0 :
				strURI = 'https://youtube.com/channel/' + strChannelID

		elif strSocialMediaType == 'instagram' :

			strUserName = ''
			if 'user' in jsonObject :
				if 'username' in jsonObject['user'] :
					strUserName = jsonObject['user']['username']

			if len(strUserName) > 0 :
				strURI = 'http://instagram.com/' + strUserName

		elif strSocialMediaType == 'foursquare' :

			# no author for venues as such (maybe use venue owner?)
			pass

		elif strSocialMediaType == 'facebook' :

			if 'from' in jsonObject :
				if 'id' in jsonObject['from'] :
					strURI = 'http://facebook.com/profile.php?id=' + jsonObject['from']['id']

		return strURI


	
	#
	# parse social media object and return its geo tag coordinates (if any)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: geo tag details (tuple)
	# e.g.
	# return tupple value = ( long, lat, POINT(long lat) )
	# - long = float
	# - lat = float
	# POINT(long lat) = string OpenGIS point 
	#
	def get_geotag( self, objSocialMediaResponse, strSocialMediaType = None ) :
		# store json object variable that will be used to extract social media geotag
		jsonObject = None
		
		# define geotag tuple variable
		tupleGeoTag = None
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :
			# handle twitter screen name detection
			if 'geo' in jsonObject :
				if jsonObject['geo'] != None :
					dictGeo = jsonObject['geo']
					
					# check the geo coordinates
					if 'coordinates' in dictGeo :
						listGeoCoordinates = dictGeo['coordinates']
						
						# check if the coordinates element is instance of list (e.g. twitter geo coordicates is a list of [lat,long])
						if isinstance( listGeoCoordinates, list ) :
							# get long and lat from the coordinates list
							# e.g. the coordinates in geo are represented in 'human readable' form (e.g. lat,lon)
							# therefore the long coordinate will be at position list[1] and lat at position list[0]
							# note: actual 'coordinates'(separate from geo) element is in geojson form (e.g. lon, lat)
							fLong = None
							fLat = None
							
							# try to get longitude and latitude from the geo coordinates element
							try :
								fLong =listGeoCoordinates[1]
								fLat = listGeoCoordinates[0]
							except :
								raise Exception( 'failed to read longitude and/or latitude from geo coordinates element (' + str( sys.exc_info()[1] ) + ')' )
							
							# construct geotag tupple
							tupleGeoTag = self.construct_geotag_tuple( fLong, fLat )
							
						else :
							self.logger.debug( 'tweet geo coordinates are invalid (must be instance of list, not' + type( listGeoCoordinates ) + ')' )
				
			else :
				self.logger.debug( 'tweet geo (e.g. geo) was not found in (' + repr( jsonObject ) + ')' )
		
		# check if json object is youtube
		# note: there is not geo location metadata in the youtube video result (the crawler will find the videos by the location,
		# but the location metadata is not included in the response!)
		elif strSocialMediaType == 'youtube' :
			tupleGeoTag = None
		
		# check if json object is instagram media item and try to get author id from it (e.g. username)
		elif strSocialMediaType == 'instagram' :
			if 'location' in jsonObject :
				dictLocation = jsonObject['location']

				# some instagram content will not have a geotag (location = null)
				if dictLocation != None :
				
					# define default longitude and latitude values
					fLong = None
					fLat = None
					
					# check the longitude value
					if 'longitude' in dictLocation :
						fLong = dictLocation['longitude']
					else :
						self.logger.debug( 'instagram media longitude (e.g. longitude) was not found in (' + repr( jsonObject ) + ')' )
					
					# check the latitude value
					if 'latitude' in dictLocation :
						fLat = dictLocation['latitude'] 
					else :
						self.logger.debug( 'instagram media latitude (e.g. latitude) was not found in (' + repr( jsonObject ) + ')' )
					
					# check if long and lat values are not None (only then construct the geotag tupple)
					if fLong is not None and fLat is not None :
						# construct geotag tupple
						tupleGeoTag = self.construct_geotag_tuple( fLong, fLat )
					else :
						self.logger.debug( 'longitude and/or latitude value can not be none' )

			else :
				self.logger.debug( 'instagram media location (e.g. location) was not found in (' + repr( jsonObject ) + ')' )	
		
		# check if json object is foursquare venue 
		elif strSocialMediaType == 'foursquare' :
			if 'location' in jsonObject :
				dictLocation = jsonObject['location']
				
				# define default longitude and latitude values
				fLong = None
				fLat = None
				
				# check the longitude value
				if 'lng' in dictLocation :
					fLong = dictLocation['lng']
				else :
					self.logger.debug( 'foursquare venue longitude (e.g. lng) was not found in (' + repr( jsonObject ) + ')' )
				
				# check the latitude value
				if 'lat' in dictLocation :
					fLat = dictLocation['lat'] 
				else :
					self.logger.debug( 'foursquare venue latitude (e.g. lat) was not found in (' + repr( jsonObject ) + ')' )
				
				# check if long and lat values are not None (only then construct the geotag tupple)
				if fLong is not None and fLat is not None :
					# finally construct geotag tupple
					tupleGeoTag = self.construct_geotag_tuple( fLong, fLat )
				else :
					self.logger.debug( 'longitude and/or latitude value can not be none' )
				
			else :
				self.logger.debug( 'foursquare venue location (e.g. location) was not found in (' + repr( jsonObject ) + ')' )
			
		# if social media will be unknown then return None
		else :
			# note: the default value is None anyway
			tupleGeoTag = None
		
		# return geo tag tuple
		return tupleGeoTag 
	
	#
	# parse social media object and return its links (web URIs and media URIs)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: list of URIs
	#
	def get_links( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		listURIs = []
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			for strTypeBase in ['entities','extended_entities'] :
				if strTypeBase in jsonObject :
					# import links of all types (web links, photos, video) 
					# extended_entities can appear under entities I think
					for strTypeLink in ['urls','media','extended_entities'] :
						if strTypeLink in jsonObject[strTypeBase] :

							# check urls
							listDict = jsonObject[strTypeBase][strTypeLink]
							if listDict != None and len( listDict ) > 0 :
								for listEntry in listDict :

									# link itself (e.g. web link or twitter embedded photo)
									if 'expanded_url' in listEntry :
										if not listEntry['expanded_url'] in listURIs :
											listURIs.append( listEntry['expanded_url'] )
									elif 'url' in listEntry :
										if not listEntry['url'] in listURIs :
											listURIs.append( listEntry['url'] )

									# link to original media (e.g. video)
									if 'media_url' in listEntry :
										if not listEntry['media_url'] in listURIs :
											listURIs.append( listEntry['media_url'] )
									elif 'media_url_https' in listEntry :
										if not listEntry['media_url_https'] in listURIs :
											listURIs.append( listEntry['media_url_https'] )

		elif strSocialMediaType == 'youtube' :

			dictSnippet = jsonObject['snippet']

			# import default OR highest res thumbnail available
			if 'thumbnails' in dictSnippet :
				bFound = False
				if bFound == False and 'high' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['high'] :
						listURIs.append( dictSnippet['thumbnails']['high']['url'] )
						bFound = True
				if bFound == False and 'medium' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['medium'] :
						listURIs.append( dictSnippet['thumbnails']['medium']['url'] )
						bFound = True
				if bFound == False and 'default' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['default'] :
						listURIs.append( dictSnippet['thumbnails']['default']['url'] )
						bFound = True

		elif strSocialMediaType == 'instagram' :

			# import standard res OR highest res image available
			if 'images' in jsonObject :
				bFound = False
				if 'standard_resolution' in jsonObject['images'] :
					if 'url' in jsonObject['images']['standard_resolution'] :
						listURIs.append( jsonObject['images']['standard_resolution']['url'] )
						bFound = True
				if bFound == False and 'low_resolution' in jsonObject['images'] :
					if 'url' in jsonObject['images']['low_resolution'] :
						listURIs.append( jsonObject['images']['low_resolution']['url'] )
						bFound = True
				if bFound == False and 'thumbnail' in jsonObject['images'] :
					if 'url' in jsonObject['images']['thumbnail'] :
						listURIs.append( jsonObject['images']['thumbnail']['url'] )
						bFound = True

		elif strSocialMediaType == 'foursquare' :

			pass

		elif strSocialMediaType == 'facebook' :

			pass

		return listURIs

	#
	# parse social media object and return its thumbnail (or None if not available)
	# only known media type4s will support this (Twitter, YouTube, Instagram, Vine)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: URI (or None)
	#
	def get_thumbnail( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		strThumbnail = None
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			# Twitter has no direct thumbnail (you can render use the sourceURI)
			pass

		elif strSocialMediaType == 'youtube' :

			dictSnippet = jsonObject['snippet']

			# use default image first, then medium and at last resort high res image URI
			if 'thumbnails' in dictSnippet :
				if strThumbnail == None and 'default' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['default'] :
						strThumbnail = dictSnippet['thumbnails']['default']['url']
				if strThumbnail == None and 'medium' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['medium'] :
						strThumbnail = dictSnippet['thumbnails']['medium']['url']
				if strThumbnail == None and 'high' in dictSnippet['thumbnails'] :
					if 'url' in dictSnippet['thumbnails']['high'] :
						strThumbnail = dictSnippet['thumbnails']['high']['url']

		elif strSocialMediaType == 'instagram' :

			# use default image first, then low and at last resort standard res image URI
			if 'images' in jsonObject :
				if strThumbnail == None and 'thumbnail' in jsonObject['images'] :
					if 'url' in jsonObject['images']['thumbnail'] :
						strThumbnail = jsonObject['images']['thumbnail']['url']
				if strThumbnail == None and 'low_resolution' in jsonObject['images'] :
					if 'url' in jsonObject['images']['low_resolution'] :
						strThumbnail = jsonObject['images']['low_resolution']['url']
				if strThumbnail == None and 'standard_resolution' in jsonObject['images'] :
					if 'url' in jsonObject['images']['standard_resolution'] :
						strThumbnail = jsonObject['images']['standard_resolution']['url']

		elif strSocialMediaType == 'foursquare' :

			pass

		return strThumbnail

	#
	# parse social media object and return its tags (tags, keywords, hashtags)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: list of URIs
	#
	def get_tags( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		listTags = []
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			if 'entities' in jsonObject :
				if 'hashtags' in jsonObject['entities'] :
					listDict = jsonObject['entities']['hashtags']
					if listDict != None and len( listDict ) > 0 :
						for listEntry in listDict :
							listTags.append( listEntry['text'] )

		elif strSocialMediaType == 'youtube' :

			# no tags in youtube search response
			pass

		elif strSocialMediaType == 'instagram' :

			if 'tags' in jsonObject :
				listTempTags = jsonObject['tags']
				if listTempTags != None and len( listTempTags ) > 0 :
					for strTag in listTempTags :
						listTags.append( strTag )

		elif strSocialMediaType == 'foursquare' :

			pass

		elif strSocialMediaType == 'facebook' :

			pass

		return listTags

	#
	# parse social media object and return its user mentions (user entities)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: list of URIs
	#
	def get_user_mentions( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		listUserMentions = []
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )
		
		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			if 'entities' in jsonObject :
				if 'user_mentions' in jsonObject['entities'] :
					listDict = jsonObject['entities']['user_mentions']
					if listDict != None and len( listDict ) > 0 :
						for listEntry in listDict :
							listUserMentions.append( listEntry['screen_name'] )

		elif strSocialMediaType == 'youtube' :

			# no user mentions in youtube search response
			pass

		elif strSocialMediaType == 'instagram' :

			# no user mentions in youtube search response
			pass

		elif strSocialMediaType == 'foursquare' :

			pass

		elif strSocialMediaType == 'facebook' :

			pass

		return listUserMentions

	#
	# parse social media object and return its text(tweet text, YT title + desc, Instagram title)
	# objSocialMediaResponse - social media response object (dict or str)
	# strSocialMediaType - optional string value that will indicate type of specified social media response json (e.g. twitter, youtube etc) (str)
	# Return: unicode string
	#
	def get_text( self, objSocialMediaResponse, strSocialMediaType = None ) :

		jsonObject = None
		strText = ''
		
		# check if the json object is instance of dict, if not try to convert json formatted string to json object
		if not isinstance( objSocialMediaResponse, dict ) :
			jsonObject = self.convert_to_json( objSocialMediaResponse )
		else :
			jsonObject = objSocialMediaResponse
		
		# double check if the jsonObject is none or empty
		if jsonObject == None :
			raise Exception( 'json object can not be none' )
		if not isinstance( jsonObject, dict ) :
			raise Exception( 'invalid json object (' + repr( jsonObject ) + ')' )
		
		# detect social media type using the json object
		# if the social media type was not specified as function parameter, then detect social media type from json object
		if strSocialMediaType == None or len( strSocialMediaType ) == 0 :
			strSocialMediaType = self.detect_social_media_type( jsonObject )

		# check if json object is twitter tweet and try to get geo details from it(if any) (e.g. geo)
		if strSocialMediaType == 'twitter' :

			strText = jsonObject['text']

		elif strSocialMediaType == 'youtube' :

			dictSnippet = jsonObject['snippet']

			# title
			strTitle = ''
			if 'title' in dictSnippet :
				strTitle = dictSnippet['title']

			# description
			strDescription = ''
			if 'description' in dictSnippet :
				strDescription = dictSnippet['description']

			strText = strTitle
			if len(strDescription) > 0 :
				if len(strText) > 0 :
					strText = strText + '\n'
				strText = strText + strDescription

		elif strSocialMediaType == 'instagram' :

			# get caption text
			if 'caption' in jsonObject :
				if jsonObject['caption'] != None :
					if 'text' in jsonObject['caption'] :
						strText = jsonObject['caption']['text']

		elif strSocialMediaType == 'foursquare' :

			# get name of venue (best guess for text)
			if 'name' in jsonObject :
				strText = jsonObject['name']

		elif strSocialMediaType == 'facebook' :

			if 'message' in jsonObject :
				strText = jsonObject['message']

		return str( strText )


	#
	# detect social media type based on passed json object
	# jsonObject - social media response object (dict or str)
	# Return: social media type, e.g. twitter, instagram etc (str)
	# Exception: thrown if fail to parse json object
	#
	def detect_social_media_type( self, jsonObject ) :
		# social media type variable that will be returned from the function
		strSocialMediaType = ''
		
		# check if the passed value is json object
		if not isinstance( jsonObject, dict ) :
			jsonObject = self.convert_to_json( jsonObject )
		
		# start detecting he social media type from the json object
		# check if json object is twitter tweet (e.g. on unique keys 'retweeted')
		if 'retweeted' in jsonObject  : 
			strSocialMediaType = 'twitter'

		# check if json object is youtube item (e.g. on unique keys 'snipper' and 'channelId'(e.g. in the snippet object))
		elif 'snippet' in jsonObject :
			strSocialMediaType = 'youtube'

		# check if json object is instagram media (e.g. on unique keys 'users_in_photo')
		elif 'users_in_photo' in jsonObject :
			strSocialMediaType = 'instagram'

		# check if json object is foursquare venue (e.g. on unique keys 'stats' and 'verified'(e.g. in the user profile settings)
		# note: 'stats and 'verified' returned in both compact and full venue response, other response fields are either optional or similar to other
		# social media types, e.g. id, name etc
		elif 'stats' in jsonObject and 'verified' in jsonObject :
			strSocialMediaType = 'foursquare'

		elif 'likes' in jsonObject :
			strSocialMediaType = 'facebook'

		else :
			strSocialMediaType = 'unknown'

		# return social media type result
		return strSocialMediaType
	
	
	#
	# helper function convert passed object to json (e.g. social media json encoded response string)
	# objSocialMediaResponse - social media response object (dict or str)
	# Return: json object
	# Exception: thrown if invalid json encoded string will be specified
	#
	def convert_to_json( self, objSocialMediaResponse ) :
		# store json object variable that will be returned from the function if all the checks will be successfully made
		jsonObject = None
		
		# check if passed object is instance of dict
		if isinstance( objSocialMediaResponse, dict ) :
			# dump json object to utf-8 encoded string (if the exception will be raised this will indicate that the json object
			# was not properly structured) 
			try :
				# create json encoded string from the object (to make sure that the json object can be properly parsed)
				strJSON = json.dumps( objSocialMediaResponse, encoding = 'utf-8' )
				
				# double check the json string value 
				if strJSON == None or len( strJSON ) == 0 :
					raise Exception( 'invalid json object is specified( ' + repr( objSocialMediaResponse ) + ')')
				
				# store jsonObject
				jsonObject = objSocialMediaResponse
			except :
				raise Exception( 'json dict object is invalid (' + str( sys.exc_info()[1] ) + ')' )
		# check if passed object is instance of string
		elif (isinstance( objSocialMediaResponse, str ) or isinstance( objSocialMediaResponse, str )) :
			try :
				# create json object from json encoded string
				jsonObject = json.loads( objSocialMediaResponse, encoding = 'utf-8' )
				
				# double check the json dict value 
				if jsonObject == None :
					raise Exception( 'json encoded string is invalid (' + str( sys.exc_info()[1] ) + ')' ) 
			except :
				raise Exception( 'json encoded string is invalid (' + str( sys.exc_info()[1] ) + ')' ) 
		else :
			raise Exception( 'passed object was not instance of dict or string : ' + str(type(jsonObject)) )
		
		# return json object if all the above checks pass
		return jsonObject
	
