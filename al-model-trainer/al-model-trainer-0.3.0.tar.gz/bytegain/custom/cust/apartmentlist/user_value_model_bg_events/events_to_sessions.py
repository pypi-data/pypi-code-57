import argparse
import logging
import apache_beam as beam
from bytegain.beam.beam_util import encode_json, DoFnWithCounters, run_pipeline, create_pipeline, get_counter
from bytegain.zap.event_utils import decode_json, _is_properties_broken
from datetime import datetime, timedelta
import math

logger = logging.getLogger('events_to_sessions')


def quantize(value, max_linear=100):
    if value > max_linear:
        normed = value * 1.0 / max_linear
        pow = int(math.log(normed, 2)) + 1
        value = int(max_linear * (2 ** pow))
    return value



class MergeEvents(DoFnWithCounters):
    """Create sessions for only users who signed up. Merge leases from _acappella_leases and events from BQ"""
    def __init__(self, only_signed, downsample_rate=1):
        super(MergeEvents, self).__init__()
        self._only_signed = only_signed
        self._downsample_rate = downsample_rate

    def process(self, xxx_todo_changeme):
        (user, data) = xxx_todo_changeme
        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp

        (_acappella_leases, _events) = data

        if user is None:
            get_counter('merge_events', 'user_id_none').inc()
            return

        # Take first 5000 events (_events is iterable), convert it to list here
        first_events = []
        for event in _events:
            if len(first_events) > 5000:
                break
            first_events.append(event)
        _events = first_events

        # Use only the first lease (one lease per user)
        first_lease = []
        for lease in _acappella_leases:
            first_lease.append(lease)
            break
        _acappella_leases = first_lease
        if _acappella_leases:
            get_counter('merge_events', 'users_with_lease').inc()

        if len(_events) > 0:
            get_counter('merge_events', 'users_with_events').inc()
            get_counter('merge_events', 'session_len_%04d' % quantize(len(_events))).inc()

            if _acappella_leases:
                get_counter('merge_events', 'users_with_events_and_lease').inc()
            lease = len(_acappella_leases) > 0

            # Find session duration and whether the user took a quiz
            signup = False
            earliest_timestamp = latest_timestamp = timestamp_to_epoch(get_timestamp(_events[0]))
            for event in _events:
                signup = event.get('context', {}).get('page', {}).get('search') == '?signup=true' or signup
                timestamp_event = timestamp_to_epoch(get_timestamp(event))
                if timestamp_event < earliest_timestamp:
                    earliest_timestamp = timestamp_event
                if timestamp_event > latest_timestamp:
                    latest_timestamp = timestamp_event

            # Counters
            if signup:
                get_counter('merge_events', 'users_with_quiz').inc()
                if _acappella_leases:
                    get_counter('merge_events', 'users_with_quiz_and_lease').inc()
            else:
                get_counter('merge_events', 'users_without_quiz').inc()

            session_duration = latest_timestamp - earliest_timestamp
            if session_duration < 60:
                get_counter('merge_events', 'session_duration_mins_00_lease_%s' % lease).inc()
            elif session_duration < 3600:
                get_counter('merge_events',
                            'session_duration_mins_%02d_lease_%s' % (session_duration / 60, lease)).inc()
            elif session_duration < 3600 * 24:
                get_counter('merge_events',
                            'session_duration_hrs_%02d_lease_%s' % (session_duration / 3600, lease)).inc()
            else:
                get_counter('merge_events', 'session_duration_days_%02d_lease_%s' % (
                session_duration / 3600 / 24, lease)).inc()
            # Downsample sessions (WARNING: this breaks p_vs_a! Prediction is not a true likelihood anymore)
            if self._downsample_rate != 1:
                if not lease and (hash(_events[-1]['timestamp']) % self._downsample_rate) != 0:
                    return
            # Use only users who:
            # 1) signed-up if `_only_signed` is set
            # 2) or all users
            if (self._only_signed and signup) or not self._only_signed:
                # Sort events by timestamp
                _events = sorted(_events + _acappella_leases, key=lambda _event: _event['timestamp'])
                yield user, _events
        else:
            get_counter('merge_events', 'users_without_events').inc()


def make_sessions(driver_input, session_generator_config, dataflow_args, output_sessions, tmp_dir):
    """
    Called by the zap driver, from the sessions stage.
    """
    p = argparse.ArgumentParser()
    args, _ = p.parse_known_args(driver_input.extra_args)

    bq_dataset = session_generator_config.get('bq_dataset')
    assert bq_dataset, 'bq_dataset must be set by the driver'

    num_shards = session_generator_config['num_shards']
    assert num_shards >= 0

    data_start_date = session_generator_config['data_start_date']
    data_end_date = session_generator_config['data_end_date']

    p = create_pipeline(dataflow_args, 'al-bg-ltv-e2s')

    t = 'acappella_leases'
    table = '`bg-event-ingester.%s.%s`' % (bq_dataset, t)
    where = " timestamp BETWEEN TIMESTAMP('{data_start_date}') AND TIMESTAMP('{data_end_date}')".format(
        data_start_date=data_start_date, data_end_date=data_end_date)
    bq_query_leases = "SELECT *, 'acappella_leases' as type FROM {table} WHERE {where}".format(table=table, where=where)

    logger.info('Leases query: %s', bq_query_leases)

    acappella_leases = (p
                        | 'read %s' %t >> beam.io.Read(
                beam.io.BigQuerySource(query=bq_query_leases, validate=True, use_standard_sql=True))
                        | 'map to userId in %s' % t >> beam.Map(lambda x: (str(x['userId']).decode('utf-8'), x))
                        )

    # Overwrite BQ query
    limit_users = session_generator_config.get('limit_users', 0)

    # For sessions don't use last X days
    end_date = datetime.strptime(data_end_date, '%Y-%m-%d')
    blackout_days = session_generator_config['blackout']
    end_date = end_date - timedelta(days=int(blackout_days))
    data_end_date_sessions = end_date.strftime('%Y-%m-%d')

    t = 'events'
    table = '`bg-event-ingester.%s.%s`' % (bq_dataset, t)
    where = "IFNULL(userId, '') <> '' AND timestamp BETWEEN TIMESTAMP('{data_start_date}') AND TIMESTAMP('{data_end_date}')".format(
        data_start_date=data_start_date, data_end_date=data_end_date_sessions)
    where += " AND (event NOT IN ('BG Scroll', 'BG Click', 'BG Click2', 'BG Key', 'bytegain_predict'))"
    if limit_users > 0:
        where += ' AND anonymousId IN (SELECT DISTINCT anonymousId FROM {table} WHERE {where} ORDER BY 1 LIMIT {limit})'.format(
            table=table, where=where, limit=limit_users)
    bq_query_events = 'SELECT * FROM {table} WHERE {where}'.format(table=table, where=where)

    logger.info('Events query: %s', bq_query_events)

    bq_events = (p
                 | 'read %s' % t >> beam.io.Read(
        beam.io.BigQuerySource(query=bq_query_events, validate=True, use_standard_sql=True))
                 | 'extract json' >> beam.Map(lambda x: x['json'])
                 | 'decode json' >> beam.Map(decode_json)
                 | 'filter bad properties' >> beam.Filter(_is_properties_broken)
                 | 'map to userId' >> beam.Map(lambda x: (x['userId'], x))
                 )

    # Merge acappella leases and bg sessions
    ((acappella_leases, bq_events) | 'group acappella leases and bg events' >> beam.CoGroupByKey()
     | 'merge and sort events' >> beam.ParDo(MergeEvents(session_generator_config['only_signed'],
                                                         downsample_rate=session_generator_config.get('downsample', 1)))
     | 'encode json' >> beam.Map(encode_json, counter=get_counter("make_sessions", "nonempty_sessions"))
     | 'save' >> beam.io.WriteToText(output_sessions, file_name_suffix='.gz', num_shards=num_shards)
     )
    counters = run_pipeline(p)

    return {'counters': counters,
            'data_end_date_sessions': data_end_date_sessions,
            'bq_query_events': bq_query_events,
            'bq_query_leases': bq_query_leases}
