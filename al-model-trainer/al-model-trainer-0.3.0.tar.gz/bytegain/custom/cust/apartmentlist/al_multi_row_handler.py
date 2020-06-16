import bytegain.custom.model_data.feature_analysis as feature_analysis
from bytegain.custom.model_data.multi_row_handler import MultiRowHandler
import tensorflow as tf

"""

import bytegain.cust.apartmentlist.al_handler_from_features as al_handler_from_features
import bytegain.model_data.read_from_db as read_from_db
selector = read_from_db.Selector("interest_web_tracks_10", None, "leased_at_notified_property", "interest_id", "original_timestamp")

row_handler = al_handler_from_features.create_multi_row_handler('web_tracks.json')
dataset =       read_from_db.create_datasets(None, 'apartmentlist', selector, row_handler)
"""

# Minimum time for event
MIN_EVENT_TIME = 0.5
INCLUDED_FEATURES = ["context_page_referrer", "event", "current_rental_id", "action", "screen_size", "label", "button_name"]
TIMESTAMP = "original_timestamp"
ID = "id"

# This makes the data files 6x as big, so disabled by default
INCLUDE_ID = False

class ALMultiRowHandler(MultiRowHandler):
    def __init__(self, feature_json, label_bucket = None, id_extractor = None):
        super(ALMultiRowHandler, self).__init__(label_bucket, id_extractor)
        features = feature_analysis.read_features(feature_json)

        for feature in features:
            if feature._column in INCLUDED_FEATURES:
                is_category = feature._datatype._datatype == str
                bucket = feature.create_bucket(is_category = is_category, none_value = -2)
                self.add_bucket(bucket)

    def extra_fields(self):
        if INCLUDE_ID:
            return [TIMESTAMP, ID]
        else:
            return [TIMESTAMP]

    def replace_field_names_with_index(self, cursor):
        super(ALMultiRowHandler, self).replace_field_names_with_index(cursor)
        header = [x.name for x in cursor.description]
        self._time_index = header.index(TIMESTAMP)
        if INCLUDE_ID:
            self._id_index = header.index(ID)

    def _create_event(self, row, elapsed):
        val = []
        for bucket in self._buckets:
            val.extend(bucket.bucketize(row))

        val.append(elapsed)
        return val

    def get_fields(self):
        fields = super(ALMultiRowHandler, self).get_fields()
        fields.append(TIMESTAMP)
        if INCLUDE_ID:
            fields.append(ID)
        return fields

    def _make_data_entry(self):
        last_time = None
        events = []
        for row in self._current_events:
            event_time = row[self._time_index]
            if last_time == None:
                last_time = event_time
                elapsed = 0
            else:
                elapsed = (event_time - last_time).seconds
                last_time = event_time
                if elapsed < MIN_EVENT_TIME:
                    continue

            events.append(self._create_event(row, elapsed))

        return events


    def make_proto_from_row_iterator(self, row_iterator):
        # Filter out later events that fired in short succession.
        def elapsed(first_row, second_row):
            return second_row[self._time_index] - first_row[self._time_index]
        filtered_rows = list(row_iterator)

        context = tf.train.Features(feature={'id': _int64_feature(self.get_id_from_row(filtered_rows[0])),
                                             'label': _int64_feature(int(self.get_label_from_row(filtered_rows[0])[0]))})

        # Add features from bucketes.
        feature_values = {bucket._name: [] for bucket in self._buckets}
        for row in filtered_rows:
            for bucket in self._buckets:
                value = bucket.bucketize(row)
                # TODO: Figure out the right way to do this.  Right now some of these ValueBuckets might actually contain -1s.
                if value == [None]:
                    value = [-1]
                feature = tf.train.Feature(int64_list=tf.train.Int64List(value=value))
                feature_values[bucket._name].append(feature)

        # Add time before next event.
        feature_values['dwell'] = []
        for i in range(len(filtered_rows) - 1):
            feature_values['dwell'].append(tf.train.Feature(int64_list=tf.train.Int64List(value=[elapsed(filtered_rows[i], filtered_rows[i + 1]), 0])))
        feature_values['dwell'].append(tf.train.Feature(int64_list=tf.train.Int64List(value=[0, 1])))

        # Add event id
        if INCLUDE_ID:
            feature_values['id'] = []
            for row in filtered_rows:
                feature_values['id'].append(tf.train.Feature(bytes_list=tf.train.BytesList(value=[row[ID]])))

        feature_lists = tf.train.FeatureLists(feature_list={k: tf.train.FeatureList(feature=v) for k, v in list(feature_values.items())})

        return tf.train.SequenceExample(context=context, feature_lists=feature_lists)

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
