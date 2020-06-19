import googlemaps
import json
import requests

from cc_py_commons.config.env import app_config
from cc_py_commons.config.pc_miler_config import PcMilerConfig
from cc_py_commons.utils.pc_miler_utils import pc_miler_limit_reached, update_pc_miler_requests_count
from cc_py_commons.utils.redis import location_db_conn, distance_db_conn, timezone_db_conn
from ast import literal_eval

def get_location(city, state, zipcode, logger):
  from_cache = False
  pc_miler_can_be_called = None
  data = __get_location_from_cache(city, state, zipcode, logger)

  if data:
    from_cache = True

  if not data:
    pc_miler_can_be_called = not pc_miler_limit_reached(logger)
    
    if pc_miler_can_be_called:
      data = __get_pc_mile_location(city, state, zipcode, logger)

  if not data:
    if not pc_miler_can_be_called:
      logger.debug("geolocate.get_location - Couldn't call PC Miler as we reached the permissible limits. Calling google.")
    else:
      logger.debug(f"geolocate.get_location - PC Miler returned no result for ({city}, {state}, {zipcode}). Calling google")

    data = __get_google_location(city, state, zipcode, logger)

  if data and not from_cache:
    __cache_location(city, state, zipcode, data, logger)

  return data

def get_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude, logger):
  if not origin_latitude or not origin_longitude or \
    not destination_latitude or not destination_longitude:
    raise Exception("Calculating distance requires both origin and destination lat/lng")

  from_cache = False
  pc_miler_can_be_called = None
  distance_cache_key = __get_distance_cache_key(origin_latitude, origin_longitude, destination_latitude, destination_longitude)

  distance = __get_distance_from_cache(distance_cache_key, logger)
  if distance:
    from_cache = True

  if not distance:
    pc_miler_can_be_called = not pc_miler_limit_reached(logger)
    
    if pc_miler_can_be_called:
      distance = __get_pc_miler_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude,
                                     logger, distance_cache_key)

  if not distance:
    if not pc_miler_can_be_called:
      logger.debug("geolocate.get_distance - Couldn't call PC Miler as we reached the permissible limits. Calling google.")
    else:
      logger.debug(f"geolocate.get_distance - PC Miler returned no result for {distance_cache_key}. Calling google")
      
    distance = __get_google_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude,
                                   logger, distance_cache_key)

  if distance and not from_cache:
    __cache_distance(distance_cache_key, distance, logger)

  return distance

def get_timezone(lat,lng, logger):
  from_cache = False
  timezone = None
  try:
    timezone_cache_key = __get_timezone_cache_key(lat, lng)
    timezone = __get_timezone_from_cache(timezone_cache_key, logger)
    if timezone:
      from_cache = True

    if not timezone:
      gmaps = googlemaps.Client(key=app_config.GOOGLE_API_KEY)
      timezone = gmaps.timezone((lat,lng))

    if timezone and not from_cache:
      __cache_timezone(timezone_cache_key, timezone, logger)
  except googlemaps.exceptions.Timeout as e:
    msg = "geolocate.get_timezone - Timezone lookup failed {0}, {1}: {2}".format(lat, lng, e)
    if logger:
      logger.error(msg)
    else:
      print(msg)

  return timezone

def __get_pc_mile_location(city, state, zipcode, logger):
  location = None
  try:
    uri = app_config.PC_MILER_URL.format("us", app_config.PC_MILER_KEY)

    if city and state:
        uri = uri + f"&city={city}&state={state}"

    if zipcode:
        uri = uri + f"&postcode={zipcode}"

    response = requests.get(uri)
    update_pc_miler_requests_count(logger)

    if response:
        locationData = json.loads(response.content)
        
        if locationData[0]['Address']:
            location = {}
            location['city'] = locationData[0]['Address']['City']
            location['state'] = locationData[0]['Address']['State']
            location['postcode'] = locationData[0]['Address']['Zip']
            location['country'] = locationData[0]['Address']['CountryAbbreviation']
            location['lat'] = float(locationData[0]['Coords']['Lat'])
            location['lng'] = float(locationData[0]['Coords']['Lon'])

  except Exception as e:
    logger.error("geolocate.__get_pc_mile_location: Error while getting location from PC Miler", e)
    location = None
  return location

def __get_pc_miler_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude,
                        logger, distance_cache_key):
  logger.debug(f"geolocate.__get_pc_miler_distance - Looking up distance from PC Miler for locations with distance_cache_key: {distance_cache_key}")
  distance = None
  try:
    pcmiler_config = PcMilerConfig()
    url = pcmiler_config.url + '?' # there is always at least on query parameter

    for key in pcmiler_config.query_params:
      if key == 'stops':
        url = f"{url}&{key}={origin_longitude},{origin_latitude};{destination_longitude},{destination_latitude}"
      elif key == 'authToken':
        url = f"{url}&{key}={app_config.PC_MILER_KEY}"
      elif pcmiler_config.query_params[key]:
        url = f"{url}&{key}={pcmiler_config.query_params[key]}"

    response = requests.get(url)
    update_pc_miler_requests_count(logger)

    if response:
      distanceData = json.loads(response.content)
      distance = distanceData[0]['TMiles']
  except Exception as e:
    logger.error("geolocate.__get_pc_miler_distance: Error while getting distance from PC Miler", e)
    distance = None
  return distance

def __get_google_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude,
                        logger, distance_cache_key):
  logger.debug(f"geolocate.__get_google_distance - Looking up distance from Google for locations with distance_cache_key: {distance_cache_key}")
  distance = None
  try:
    gmaps = googlemaps.Client(key=app_config.GOOGLE_API_KEY)
    origins = [f'{origin_latitude} {origin_longitude}']
    destinations = [f'{destination_latitude} {destination_longitude}']
    response = gmaps.distance_matrix(origins,destinations,mode="driving",units="imperial")
    if response:
      distance_in_meters = response['rows'][0]['elements'][0]['distance']['value']
      distance = distance_in_meters / 1609
  except Exception as e:
    logger.error("geolocate.__get_google_distance: Error while getting distance from google", e)
    distance = None
  return distance

def __get_google_location(city, state, zipcode, logger):
  try:
    loc_str = ''

    if city:
      loc_str = city

    if state:
      if len(loc_str) > 0:
        loc_str = loc_str + ', '

      loc_str = loc_str + state

    if zipcode:
      if len(loc_str) > 0:
        loc_str = loc_str + ' '

      loc_str = loc_str + zipcode

    gmaps = googlemaps.Client(key=app_config.GOOGLE_API_KEY)
    response = gmaps.geocode(loc_str)

    if response:
      data = { 'city': None, 'state': None, 'postcode': None }
      components = response[0]['address_components']
      location = response[0]['geometry']['location']

      for component in components:
        if 'locality' in component['types']:
          data['city'] = component['short_name']
        elif 'administrative_area_level_1' in component['types']:
          data['state'] = component['short_name']
        elif 'postcode' in component['types']:
          data['postcode'] = component['short_name']
        elif 'country' in component['types']:
          data['country'] = component['short_name']

      data['lat'] = location['lat']
      data['lng'] = location['lat']
      return data
  except googlemaps.exceptions.Timeout as e:
    msg = "geolocate.__get_google_location - Location lookup timed out {0}, {1}, {2}: {3}".format(city, state, zipcode, e)

    if logger:
      logger.error(msg)
    else:
      print(msg)
  except googlemaps.exceptions.HTTPError as e:
    msg = "geolocate.__get_google_location - Location lookup failed {0}, {1}, {2}: {3}".format(city, state, zipcode, e)

    if logger:
      logger.error(msg)
    else:
      print(msg)

  return None

def __cache_location(city, state, zipcode, location_data, logger):
  location_string = __get_location_string(city, state, zipcode)
  logger.debug(f'geolocate.__cache_location - caching location: {location_string} with location data: {location_data}')
  location_db_conn.set(location_string, str(location_data))

def __get_location_from_cache(city, state, zipcode, logger):
  location_string = __get_location_string(city, state, zipcode)
  response = location_db_conn.get(location_string)
  if response:
    response = literal_eval(response.decode('utf-8'))
  logger.debug(f'geolocate.__get_location_from_cache - location : {location_string} has cached value: {response}')
  return response

def __get_location_string(city, state, zipcode):
  location_string = ''
  if city:
    location_string += ('_'.join(city.split(' ')))
  if state:
    location_string += f'_{state}'
  if zipcode:
    location_string += f'_{zipcode}'

  return location_string.lower()

def __cache_distance(distance_cache_key, distance, logger):
  logger.debug(f'geolocate.__cache_distance - caching distance: {distance} for distance_cache_key: {distance_cache_key}')
  distance_db_conn.set(distance_cache_key, distance)

def __get_distance_from_cache(distance_cache_key, logger):
  distance = None
  try:
    distance = distance_db_conn.get(distance_cache_key)
    if distance:
      distance = float(distance)
    logger.debug(f'geolocate.__get_distance_from_cache - distance_cache_key : {distance_cache_key} has cached value: {distance}')
  except Exception as e:
    logger.debug("geolocate.__get_distance_from_cache: Error while getting distance from cache", e)
    distance = None
  return distance

def __get_distance_cache_key(origin_latitude, origin_longitude, destination_latitude, destination_longitude):
  return f'{__truncate(origin_latitude)},{__truncate(origin_longitude)}->{__truncate(destination_latitude)},{__truncate(destination_longitude)}'

def __truncate(number):
  return int(number * 1000000) / 1000000

def __cache_timezone(timezone_cache_key, timezone, logger):
  logger.debug(f'geolocate.__cache_timezone - caching timezone: {timezone} for timezone_cache_key: {timezone_cache_key}')
  timezone_db_conn.set(timezone_cache_key, timezone)

def __get_timezone_from_cache(timezone_cache_key, logger):
  timezone = None
  try:
    timezone = timezone_db_conn.get(timezone_cache_key)
    if timezone:
      timezone = literal_eval(timezone.decode('utf-8'))
    logger.debug(f'geolocate.__get_timezone_from_cache - timezone_cache_key : {timezone_cache_key} has cached value: {timezone}')
  except Exception as e:
    logger.debug("geolocate.__get_timezone_from_cache - Error while getting timezone from cache", e)
    timezone = None
  return timezone

def __get_timezone_cache_key(lat,lng):
  return f'{lat},{lng}'
