from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query

class LiveStream:
  live_stream_base = WSC_API_ENDPOINT + 'live_streams'
  live_stream_single = live_stream_base + '/{live_stream_id}'         # live_stream delete, get
  live_stream_single_state = live_stream_single + '/state'            # live_stream state
  live_stream_single_start = live_stream_single + '/start'            # live_stream start
  live_stream_single_stop = live_stream_single + '/stop'              # live_stream stop
  live_stream_single_stats = live_stream_single + '/stats'                  # live_stream stats
  live_stream_single_thumbnail_url = live_stream_single + '/thumbnail_url'  # live_stream thumbnail_url

  @classmethod
  def create_live_stream(cls, data):
    # Create wowza live stream 
    response = wowza_query(endpoint=cls.live_stream_base, method='post', data=data)
    return response['live_stream']

  @classmethod
  def update_live_stream(cls, live_stream_id, data):
    endpoint = cls.live_stream_single.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint=endpoint, method='patch', data=data)
    return response['live_stream']

  @classmethod
  def get_live_streams(cls):
    # Get the list of live stream
    response = wowza_query(endpoint=cls.live_stream_base, method='get')
    live_streams = response['live_streams']
    logger.debug('Live streams are {}'.format(live_streams))
    return live_streams

  @classmethod
  def get_live_stream(cls, live_stream_id):
    # Get info of a live stream
    endpoint = cls.live_stream_single.format(
      live_stream_id=live_stream_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    live_stream = response['live_stream']
    logger.debug('Live stream info is {}'.format(live_stream))
    return live_stream

  @classmethod
  def get_state(cls, live_stream_id):
    endpoint = cls.live_stream_single_state.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']['state']
    return state

  @classmethod
  def start_live_stream(cls, live_stream_id):
    endpoint = cls.live_stream_single_start.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'put')
    state = response['live_stream']['state']
    return state
  
  @classmethod
  def stop_live_stream(cls, live_stream_id):
    endpoint = cls.live_stream_single_stop.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'put')
    state = response['live_stream']['state']
    return state

  @classmethod
  def get_thumbnail_url(cls, live_stream_id):
    endpoint = cls.live_stream_single_thumbnail_url.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']['thumbnail_url']
    return state

  @classmethod
  def get_stats(cls, live_stream_id):
    endpoint = cls.live_stream_single_stats.format(live_stream_id=live_stream_id)
    response = wowza_query(endpoint, 'get')
    state = response['live_stream']
    return state