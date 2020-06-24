from wowpy.livestreams import LiveStream
from wowpy.transcoders import Transcoder
from wowpy.targets import TargetStream

def get_resource_info(id):
  resource_info = {
    'input': {
      'livestream': {}
    },
    'output': {
      'transcoder': {},
      'targets': []
    },
    'schedule': {}
  }

  live_stream = LiveStream.get_live_stream(id)
  resource_info['input']['livestream'] = live_stream
  transcoder_info = Transcoder.get_transcoder(id)
  resource_info['output']['transcoder'] = transcoder_info
  stream_targets = live_stream['stream_targets']
  for stream_target in stream_targets:
    stream_target_id = stream_target['id']
    stream_target_info = TargetStream.get_target(stream_type='custom', stream_target_id=stream_target_id)
    stream_target_properties = TargetStream.get_target_properties(stream_type='custom', stream_target_id=stream_target_id)
    resource_info['output']['targets'].append({'config': stream_target_info, 'properties': stream_target_properties})

#   schedule_info = Schedule.get_schedule(scheduler_id=scheduler_id)
#   resource_info['schedule'] = schedule_info

  return resource_info