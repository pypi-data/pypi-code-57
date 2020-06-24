from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query
  
class Transcoder:
  transcoder_base = WSC_API_ENDPOINT + 'transcoders/{transcoder_id}'             # transcoder update timeout
  transcoder_start = transcoder_base + '/start'                                  # transcoder start
  transcoder_stop = transcoder_base + '/stop'                                    # transcoder stop
  transcoder_reset = transcoder_base + '/reset'                                  # transcoder reset
  transcoder_outputs = transcoder_base + '/outputs'                              # transcoder read/write outputs
  transcoder_output_single = transcoder_outputs + '/{output_id}'                 # transcoder output update, delete
  transcoder_targets = transcoder_outputs + '/{output_id}/output_stream_targets' # transcoder associate
  transcoder_target_single = transcoder_targets + '/{stream_target_id}'          # transcoder delete target 

  @classmethod
  def get_transcoder_outputs(cls, transcoder_id):
    # Get outputs for a transcoder
    endpoint = cls.transcoder_outputs.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    return response['outputs']

  @classmethod
  def update_transcoder(cls, transcoder_id, data):
    # Update transcoder timeout
    endpoint = cls.transcoder_base.format(
      transcoder_id=transcoder_id
    )
    wowza_query(endpoint=endpoint, method='patch', data=data)

  @classmethod
  def delete_target(cls, transcoder_id, output_id, stream_target_id):
    # Delete stream target created by wowza
    endpoint = cls.transcoder_target_single.format(
      transcoder_id=transcoder_id, 
      output_id=output_id, 
      stream_target_id=stream_target_id
    )
    wowza_query(endpoint=endpoint, method='delete')

  @classmethod
  def create_transcoder_output(cls, transcoder_id, data):
    # Add an output to the transcoder
    endpoint = cls.transcoder_outputs.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='post', data=data)
    return response['output']['id']

  @classmethod
  def delete_transcoder_output(cls, transcoder_id, output_id):
    endpoint = cls.transcoder_output_single.format(transcoder_id=transcoder_id, output_id=output_id)
    wowza_query(endpoint=endpoint, method='delete')

  @classmethod
  def update_transcoder_output(cls, transcoder_id, output_id, data):
    endpoint = cls.transcoder_output_single.format(transcoder_id=transcoder_id, output_id=output_id)
    response = wowza_query(endpoint=endpoint, method='patch', data=data)
    return response['output']

  @classmethod
  def associate_target_stream(cls, transcoder_id, output_id, stream_target_id):
    # Associate a target with a live stream
    data = {
      'output_stream_target': {
        'stream_target_id': stream_target_id,
        'use_stream_target_backup_url': 'false'
      }
    }
  
    endpoint = cls.transcoder_targets.format(
      transcoder_id=transcoder_id, 
      output_id=output_id
    )
    wowza_query(endpoint=endpoint, method='post', data=data)

  @classmethod
  def get_transcoder(cls, transcoder_id):
    endpoint = cls.transcoder_base.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    transcoder = response['transcoder']
    return transcoder

  @classmethod
  def start_transcoder(cls, transcoder_id):
    endpoint = cls.transcoder_start.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='put')
    transcoder = response['transcoder']
    return transcoder

  @classmethod
  def stop_transcoder(cls, transcoder_id):
    endpoint = cls.transcoder_stop.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='put')
    transcoder = response['transcoder']
    return transcoder

  @classmethod
  def reset_transcoder(cls, transcoder_id):
    endpoint = cls.transcoder_reset.format(
      transcoder_id=transcoder_id
    )
    response = wowza_query(endpoint=endpoint, method='put')
    transcoder = response['transcoder']
    return transcoder
