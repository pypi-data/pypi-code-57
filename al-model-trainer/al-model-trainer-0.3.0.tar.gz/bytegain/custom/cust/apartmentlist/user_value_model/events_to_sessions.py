"""
Transform events into user sessions.

Input should be a top level directory, e.g. 'gs://bg-dataflow/all_features' containing sub-folders
'/web_pages/' and 'lead_scoring_lead_scoring_set/'. Each of them should contain compressed .cvs
files and a pickle file with TableInfo
"""

import argparse
import json
import logging
import apache_beam as beam
from bytegain.beam.beam_util import encode_json, DoFnWithCounters, run_pipeline, create_pipeline, get_counter
from bytegain.zap.utils import gcs

from bytegain.custom.model_data.schema_from_TableInfo import get_schema

logger = logging.getLogger('events_to_sessions')


class MakeDict(DoFnWithCounters):
    """
        Convert csv rows into a dictionary and map columns to specific zap-compatible fields
    """

    def __init__(self, table_info):
        super(MakeDict, self).__init__()
        # Map keys for consistency with zap
        self._key_map = {'user_id': 'userId',
                         'anonymous_id': 'anonymousId',
                         'received_at': 'timestamp',
                         'value_at': 'timestamp',
                         'created_at': 'timestamp',
                         'context_page_title': 'title',
                         'referrer': ['context', 'page', 'referrer'],
                         'context_page_url': ['context', 'page', 'url'],
                         'context_user_agent': ['context', 'userAgent'],
                         'context_page_path': ['context', 'page', 'path'],
                         'context_page_referrer': ['context', 'page', 'referral'],
                         'context_page_search': ['context', 'page', 'search'],
                         'notified_at': 'timestamp',
                         'leased_at_notified_property': 'label',
                         'original_timestamp': 'originalTimestamp',
                         'context_library_version': ['library', 'version'],
                         'context_library_name': ['library', 'name'],
                         # 'name': 'title'
                         # it seems like 'name' is the only useful feature in '*.screens' table,
                         # let's map it to 'title'
                         }
        self._columns = []
        for column in table_info.columns:
            col_name = column.name
            if col_name in self._key_map:
                col_name = self._key_map[col_name]
            self._columns.append(col_name)

    def nested_set(self, dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    def process(self, row):
        dict = self._make_dict(row)
        if dict:
            yield dict

    def _make_dict(self, row):
        import csv
        values = next(csv.reader([row.encode('utf-8')], delimiter='|', escapechar='\\'))
        values = [str(val, 'utf-8') for val in values]
        row_dict = {}
        if len(self._columns) != len(values):
            self.get_counter('bad_row').inc()
            logging.info('Bad row: %s' % row)
            return
        for c, key in enumerate(self._columns):
            if type(key) is not list:
                key = [key]
            self.nested_set(row_dict, key, values[c])
        try:
            return row_dict
        except Exception as e:
            print("Bad line: %s" % row)
            raise e


class MergeEventsFeatures(DoFnWithCounters):
    """
        Create a user session: merge events, assign types and sort them by timestamp
    """
    def __init__(self):
        super(MergeEventsFeatures, self).__init__()

    def process(self, xxx_todo_changeme):
        (user, data) = xxx_todo_changeme
        from bytegain.beam.beam_util import get_counter

        (_web_pages, _features, _acappella_leases, _ios_screens, _android_screens, _interest, _web_compass) = data
        # Make all events as 'page' for compatibility with the zap pipeline
        for p in _web_pages:
            p['type'] = 'page'

        _events = _web_pages

        for s in _ios_screens:
            s['type'] = 'screen'

        _events += _ios_screens

        for s in _android_screens:
            s['type'] = 'screen'

        _events += _android_screens

        for c in _web_compass:
            c['type'] = 'compass'

        _events += _web_compass

        # try interest as a page
        # _events += _interest

        if len(_events) == 0:
            get_counter('sessions', 'users_without_events').inc()
            return
        else:
            get_counter('sessions', 'users_with_events').inc()

        # Mark other events as different types (they will be filtered out via rows_filter)
        for f in _features:
            get_counter('session', 'feature').inc()
            f['type'] = 'features'
        for l in _acappella_leases:
            get_counter('session', 'acappella_lease').inc()
            l['type'] = 'acappella_lease'

        # Now merge features, acappella leases into events
        _events += _features
        _events += _acappella_leases

        # Sort events by timestamp
        _events = sorted(_events, key=lambda _event: _event['timestamp'])
        yield user, _events


def make_sessions(driver_input, session_generator_config, dataflow_args, output_sessions, tmp_dir):
    """
    Called by the zap driver, from the sessions stage.
    """
    p = argparse.ArgumentParser()
    p.add_argument('--redshift_data', required=(driver_input.command == 'predict'), help='GCS URL to an existing Redshift data import')
    p.add_argument('--redshift_training_data', required=True, help='GCS URL to an existing Redshift data used in '
                                                                   'training')
    p.add_argument('--sessions_num_shards', type=int, default=-1, help='Override default num_shards')
    args, _ = p.parse_known_args(driver_input.extra_args)

    redshift_training_data = args.redshift_training_data.rstrip('/')
    logger.info('Redshift training data: %s', redshift_training_data)

    redshift_data = args.redshift_data.rstrip('/') if driver_input.command == 'predict' else redshift_training_data
    logger.info('Redshift data: %s', redshift_data)

    num_shards = args.sessions_num_shards if args.sessions_num_shards >= 0 else session_generator_config['num_shards']
    session_generator_config['num_shards'] = num_shards
    logger.info('Num shards: %s', num_shards)

    # Data start and end dates come from a json file written by the data importer tool. Read the file early, if it
    # doesn't exist it's a sign the import job didn't make it to the end.
    dates = json.loads(gcs.get_file_contents_as_string(redshift_data + '/data_start_end_dates.json'))
    data_start_date = dates['data_start_date']
    assert data_start_date
    data_end_date = dates['data_end_date']
    assert data_end_date
    # Update session_generator_config so that the driver can track the dates
    session_generator_config['data_start_date'] = data_start_date
    session_generator_config['data_end_date'] = data_end_date

    # Extract schemas from training dataset
    subdirs = {
        'web_pages': '/web_pages/',
        'features': '/ml_notified_training_set/',
        'acappella_leases': '/etl_acappella_leases/',
        'ios_screens': '/ios_screens/',
        'android_screens': '/android_screens/',
        'interest': '/api_interest/',
        'web_compass': '/web_compass/'
    }
    if driver_input.command == 'predict':
        subdirs['features'] = '/ml_notified_features/'
    schemas = get_schema(redshift_data, subdirs)

    # TODO (yuri): Create buckets somewhere here

    p = create_pipeline(dataflow_args, 'al-events-to-sessions')

    tables = ['web_pages', 'features', 'acappella_leases', 'ios_screens', 'android_screens', 'interest', 'web_compass']
    data = []
    for key in tables:
        data.append(
            (p
             | 'read %s' % key >> beam.io.ReadFromText(redshift_data + subdirs[key] + '*.gz')
             | 'make %s dict' % key >> beam.ParDo(MakeDict(table_info=schemas[key]))
             | 'map %s to userId' % key >> beam.Map(lambda x: (x['userId'], x))
             )
        )

    _ = (data | beam.CoGroupByKey()
            | 'merge events' >> beam.ParDo(MergeEventsFeatures())
            | 'ignore empty and large sessions' >> beam.Filter(lambda user__events: 0 < len(user__events[1]) < 1000)
            # 1000 is an arbitrary cutoff
            | 'encode json' >> beam.Map(encode_json, counter=get_counter("make_sessions", "nonempty_sessions"))
            | 'save' >> beam.io.WriteToText(output_sessions, file_name_suffix='.gz', num_shards=num_shards)
            )

    counters = run_pipeline(p)

    return {'counters': counters,
            'redshift_data': redshift_data,
            'redshift_training_data': redshift_training_data}
