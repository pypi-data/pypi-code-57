import json

from worker.framework.mixins import RedisMixin


def file_to_json(file_name):
    with open(file_name, mode='r') as file:
        _json = json.load(file)
        return _json


def get_last_processed_timestamp(redis_key: str):
    """
    Get the last_processed_timestamp from the redis key
    :param redis_key: redis key
    """
    try:
        r = RedisMixin().get_redis()
        previous_state = r.get(redis_key)

        if previous_state is None:
            return None

        previous_state = json.loads(previous_state)
        return previous_state.get('last_processed_timestamp', None)
    except Exception as ex:
        print(f"Error occurred while reading state from Redis!\nError: {ex}")

    return None


def create_scheduler_events(asset_id, start_timestamp, end_timestamp, step):
    """
    Creating scheduler events
    :param asset_id:
    :param start_timestamp:
    :param end_timestamp:
    :param step:
    :return:
    """
    if start_timestamp > end_timestamp:
        raise ValueError(f"start_timestamp ({start_timestamp}) is greater than end_timestamp ({end_timestamp})!")
    if step <= 0 or step > 3600:
        raise ValueError(f"step ({step}) is outside the (0, 3600] range.")

    triggers = range(start_timestamp, end_timestamp, step)
    events = [[[{"asset_id": asset_id, "schedule_start": 1000 * trigger, "schedule_end": 1000 * (trigger + step)}]]
              for trigger in triggers]
    return events
