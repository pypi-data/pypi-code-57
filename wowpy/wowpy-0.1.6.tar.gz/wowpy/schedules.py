import dateutil.parser
from datetime import timedelta
from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query, safe_run

class Schedule:

  scheduler_base = WSC_API_ENDPOINT + 'schedules'
  scheduler_single = scheduler_base + '/{scheduler_id}'  # get ,delete, update

  @classmethod
  def create_schedule(cls, data):
    response = wowza_query(endpoint=cls.scheduler_base, method='post', data=data)
    schedule = response['schedule']
    return schedule

  @classmethod
  def get_schedules(cls):
    # Get the list of schedules
    response = wowza_query(endpoint=cls.scheduler_base, method='get')
    logger.debug('Schedules response is {}'.format(response))
    schedules = response['schedules']
    return schedules

  @classmethod
  def get_schedule(cls, scheduler_id):
    endpoint = cls.scheduler_single.format(scheduler_id=scheduler_id)
    response = wowza_query(endpoint, 'get')
    schedule = response['schedule']
    return schedule

  @classmethod
  def delete_schedule(cls, scheduler_id):
    endpoint = cls.scheduler_single.format(scheduler_id=scheduler_id)
    response = wowza_query(endpoint, 'delete')
    schedule = response['schedule']
    return schedule

  @classmethod
  def update_schedule(cls, scheduler_id, data):
    endpoint = cls.scheduler_single.format(scheduler_id=scheduler_id)
    response = wowza_query(endpoint=endpoint, method='patch', data=data)
    schedule = response['schedule']
    return schedule

  @classmethod
  def process_schedule_data(cls, data, time_before=0, time_after=0):
    start_time = data['schedule']['start_transcoder']
    stop_time = data['schedule'].get('stop_transcoder', None)

    start_transcoder = dateutil.parser.parse(start_time) - timedelta(minutes=time_before)
    start_transcoder_iso = start_transcoder.strftime("%Y-%m-%dT%H:%M:%S.%fZ") # ISO 8601 datetime

    if stop_time:
      stop_transcoder = dateutil.parser.parse(stop_time) + timedelta(minutes=time_after)
    else: # not stop_transcoder specified
      stop_transcoder = dateutil.parser.parse(start_time) + timedelta(minutes=time_after)
    stop_transcoder_iso = stop_transcoder.strftime("%Y-%m-%dT%H:%M:%S.%fZ") # ISO 8601 datetime

    data['schedule']['start_transcoder'] = start_transcoder_iso
    data['schedule']['stop_transcoder'] = stop_transcoder_iso

    return data