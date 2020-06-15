from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query

class Livestream:
  livestream_base = WSC_API_ENDPOINT + 'live_streams'
  livestream_single = livestream_base + '/{live_stream_id}'         # livestream delete, get
  livestream_single_state = livestream_single + '/state'            # livestream state
  livestream_single_start = livestream_single + '/start'            # livestream start
  livestream_single_stop = livestream_single + '/stop'              # livestream stop
  livestream_single_stats = livestream_single + '/stats'                  # livestream stats
  livestream_single_thumbnail_url = livestream_single + '/thumbnail_url'  # livestream thumbnail_url

  @classmethod
  def create_livestream(cls, data):
    # Create wowza livestream 
    response = wowza_query(endpoint=cls.livestream_base, method='post', data=data)
    return response['live_stream']

  @classmethod
  def update_livestream(cls, live_stream_id, data):
    endpoint = cls.livestream_single.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint=endpoint, method='patch', data=data)
    return response['live_stream']

  @classmethod
  def get_livestreams(cls):
    # Get the list of livestream
    response = wowza_query(endpoint=cls.livestream_base, method='get')
    live_streams = response['live_streams']
    logger.debug('Livestream are {}'.format(live_streams))
    return live_streams

  @classmethod
  def get_livestream(cls, live_stream_id):
    # Get info of a livestream
    endpoint = cls.livestream_single.format(
      live_stream_id=live_stream_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    live_stream = response['live_stream']
    logger.debug('Livestream info is {}'.format(live_stream))
    return live_stream

  @classmethod
  def get_state(cls, live_stream_id):
    endpoint = cls.livestream_single_state.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']['state']
    return state

  @classmethod
  def start_livestream(cls, live_stream_id):
    endpoint = cls.livestream_single_start.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'put')
    state = response['live_stream']['state']
    return state
  
  @classmethod
  def stop_livestream(cls, live_stream_id):
    endpoint = cls.livestream_single_stop.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'put')
    state = response['live_stream']['state']
    return state

  @classmethod
  def get_thumbnail_url(cls, live_stream_id):
    endpoint = cls.livestream_single_thumbnail_url.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']['thumbnail_url']
    return state

  @classmethod
  def get_stats(cls, live_stream_id):
    endpoint = cls.livestream_single_stats.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']
    return state