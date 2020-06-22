from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query

class TargetStream:

  custom_data = {}
  stream_target_base = WSC_API_ENDPOINT + 'stream_targets' 
  stream_target_type = stream_target_base + '/{stream_type}'
  stream_target_single = stream_target_type + '/{stream_target_id}'                     # target delete, get, update
  stream_target_properties = stream_target_base + '/{stream_target_id}' + '/properties' # target properties

  @classmethod
  def create_target(cls, data):
    endpoint = cls.stream_target_type.format(stream_type='custom')
    response = wowza_query(endpoint=endpoint, method='post', data=data)
    stream_target_id = response['stream_target_custom']['id']
    return stream_target_id

  # Update target: primary url, stream name
  @classmethod
  def update_target(cls, stream_target_id, target_data):
    endpoint = cls.stream_target_single.format(stream_type='custom', stream_target_id=stream_target_id)
    response = wowza_query(endpoint=endpoint, method='patch', data=target_data)
    stream_target_id = response['stream_target_custom']['id']
    return stream_target_id

  # Update stream target properties
  @classmethod
  def update_properties(cls, stream_target_id, properties_data):
    for property_data in properties_data:
      cls.update_property(stream_target_id=stream_target_id, data=property_data)

  @classmethod
  def update_property(cls, stream_target_id, data):
    endpoint = cls.stream_target_properties.format(stream_target_id=stream_target_id)
    properties_response = wowza_query(endpoint=endpoint, method='post', data=data)
    return properties_response['property']

  @classmethod
  def get_targets(cls, stream_type):
    # Get the list of custom stream targets
    endpoint = cls.stream_target_type.format(stream_type=stream_type)
    response = wowza_query(endpoint=endpoint, method='get')
    return response['stream_targets_'+stream_type]

  @classmethod
  def delete_targets(cls, stream_type, stream_target_ids):
    # Delete custom target streams
    for stream_target_id in stream_target_ids:
      cls.delete_target(stream_type=stream_type,
                        stream_target_id=stream_target_id)

  # if we change a Live stream name, baton is not going to be able to delete it
  # so the Live stream will exist when we try to delete the target, causing a wowza
  # exception 
  @classmethod
  def delete_target(cls, stream_type, stream_target_id):
    try:
      # Delete a stream target
      endpoint = cls.stream_target_single.format(stream_type=stream_type,
                                                  stream_target_id=stream_target_id)
      wowza_query(endpoint=endpoint, method='delete')
    except Exception as excp:
      logger.info('Target with id {stream_target_id} can not be deleted, please delete it manually, {excp}'.format(
        stream_target_id=stream_target_id,
        excp=excp)
      )

  @classmethod
  def get_target(cls, stream_type, stream_target_id):
    endpoint = cls.stream_target_single.format(stream_type=stream_type,
                                              stream_target_id=stream_target_id)
    response = wowza_query(endpoint=endpoint, method='get')
    stream_target = response['stream_target_custom']
    return stream_target
    
  @classmethod
  def get_target_properties(cls, stream_type, stream_target_id):
    endpoint = cls.stream_target_properties.format(stream_target_id=stream_target_id)
    response = wowza_query(endpoint=endpoint, method='get')
    return response['properties']