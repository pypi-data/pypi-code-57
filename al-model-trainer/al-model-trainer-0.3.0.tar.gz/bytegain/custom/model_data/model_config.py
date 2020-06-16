""" Holds a model configuration.

To build a ModelConfig from a SchemaInfo:

from bytegain.model_data.model_config import ModelConfig
ModelConfig.from_table_info_file('web_join2.pickle').to_json_file('model_configs/al_1.0')

"""

import pyximport

from bytegain.zap.prediction_instance import PredictionInstance, set_counter_impl

pyximport.install()

import pickle
import datetime
import json
import tensorflow as tf
import random

from bytegain.data_import.segment_utils import timestamp_to_epoch
from bytegain.zap import feature_coding
from bytegain.custom.model_data.bucket import SimpleCategoricalBucket, ValueBucket
from collections import OrderedDict
import importlib

def get_epoch_times_for_rows(rows):
    row_dt = []
    for i in range(0, len(rows)):
        row_dt.append(datetime.datetime.utcfromtimestamp(timestamp_to_epoch(rows[i]['timestamp'])))
    return row_dt


class ModelConfigFeature(object):
    # TODO(chris): Support non-categorical.
    def __init__(self, field, categories):
        self._field = field
        self._categories = categories

    @staticmethod
    def from_column_info(column_info, table_name = None):
        """ Construct a feature from ColumnInfo.

        If table_name is set, it is used to create a new feature name.

        Returns None if the column is not supported.
        """
        name = column_info.name

        # TODO(chris): Stop peeking into internal _groups.
        if not column_info.is_groupable() or not column_info._groups or column_info.required() or len(column_info._groups) < 2:
            return None
        # name = ("%s_%s" % (table_name, column_info.name)) if table_name is not None else column_info.name
        # print ("Including: %s.%s" % (table_name, column_info))
        if column_info.name == "event":
            # Hack so we capture all events since they are usually used in prediction instance
            group_limit = 0.00001
        else:
           # The minimum ratio for a group is g[1]/20 - this prevents tons of outliers on the tail.
            # It's g[1] not g[0] since g[0] is often null
            group_limit = max(column_info._groups[1][1] / 20.0, 0.0001)

        groups = [g[0] for g in column_info._groups if g[1] > group_limit]

        # If null_fraction > last_group fraction then add a None
        if column_info.null_fraction > column_info._groups[-1][1] and None not in groups:
            groups.append(None)

        if len(groups) < 2 and "char" in column_info.datatype:
            return None
        return ModelConfigFeature(name, groups)

    @staticmethod
    def merge_features(feature1, feature2):
        assert feature1._field == feature2._field
        categories = set(feature1._categories)
        categories.update(feature2._categories)
        return ModelConfigFeature(feature1._field, [g for g in categories])

    @staticmethod
    def from_dict(rep):
        return ModelConfigFeature(rep['field'], rep['categories'])

    def to_dict(self):
        return OrderedDict([
                ('field', self._field),
                ('categories', self._categories)])

    @property
    def field(self):
        return self._field

    @property
    def categories(self):
        return self._categories

class ModelConfigEventSelector(object):
    def __init__(self, fields, expression):
        self._fields = fields
        self._expression = expression

    @staticmethod
    def from_dict(rep):
        return ModelConfigEventSelector(rep['fields'], rep['expression'])

    def to_dict(self):
        return OrderedDict([
                ('fields', self._fields),
                ('expression', self._expression)])

    @property
    def fields(self):
        return self._fields

    @property
    def expression(self):
        return self._expression

class ModelConfig(object):
    """ Configuration for training a clickstreaam model from a sequence of events. """
    def __init__(self, id_field, instance_generator, blackout_seconds, negative_fraction, features, timestamp_field = 'received_at', max_events = 40):
        self._id_field = id_field
        self._instance_generator = instance_generator
        self._blackout_seconds = blackout_seconds
        self._negative_fraction = negative_fraction
        self._timestamp_field = timestamp_field
        self._features = features
        self._max_events = max_events

        # Maximum time between duplicate events
        self._dup_max_time = 3

    @staticmethod
    def from_schema_info_file(path):
        instance_generator = 'UNCONFIGURED'
        from bytegain.custom.data_import.schema_info import read_schema_from_file as read_schema_info_from_file
        schema_info = read_schema_info_from_file(path)

        # Maps from column.name -> Feature
        # Used to merge multiple columns with same name
        feature_dict = {}
        for column in schema_info.main_table.columns:
            feature = ModelConfigFeature.from_column_info(column)
            if feature:
                feature_dict[column.name] = feature
        for column in schema_info.page_table.columns:
            feature = ModelConfigFeature.from_column_info(column, schema_info.page_table.table)
            if feature:
                if column.name in feature_dict:
                    feature = ModelConfigFeature.merge_features(feature_dict[column.name], feature)
                feature_dict[column.name] = feature

        for table_info in list(schema_info.join_tables.values()):
            for column in table_info.columns:
                feature = ModelConfigFeature.from_column_info(column, table_info.table)
                if feature:
                    if column.name in feature_dict:
                        feature = ModelConfigFeature.merge_features(feature_dict[column.name], feature)
                    feature_dict[column.name] = feature

        features = sorted(list(feature_dict.values()), key = lambda v : v._field)
        return ModelConfig('UNCONFIGURED', instance_generator, 1.0, 1.0, features)

    @staticmethod
    def from_table_info_file(path):
        table_info = pickle.load(open(path, 'rb'))
        features = []
        for column in table_info.columns:
            feature = ModelConfigFeature.from_column_info(column)
            if feature:
                features.append(feature)
        return ModelConfig('UNCONFIGURED', 'UNCONFIGURED', 1.0, 1.0, 'UNCONFIGURED', features)

    @staticmethod
    def from_json_file(path):
        with open(path) as f:
            jrep = json.load(f)
            return ModelConfig.from_dict(jrep)

    @staticmethod
    def from_dict(jrep):
        features = [ModelConfigFeature.from_dict(feature_rep) for feature_rep in jrep['features']]
        return ModelConfig(jrep['idField'], jrep['instanceGenerator'],
                        jrep['blackoutSeconds'], jrep['negativeFraction'], features, jrep['timestampField'], jrep['maxEvents'])

    def set_params(self, id_field, timestamp_field, instance_generator, max_events, blackout_seconds):
        self._id_field = id_field
        self._timestamp_field = timestamp_field
        self._instance_generator = instance_generator
        self._max_events = max_events
        self._blackout_seconds = blackout_seconds

    def to_json_file(self, path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        return OrderedDict([
                ('idField', self._id_field),
                ('instanceGenerator', self._instance_generator),
                ('blackoutSeconds', self._blackout_seconds),
                ('negativeFraction', self._negative_fraction),
                ('timestampField', self._timestamp_field),
                ('maxEvents', self._max_events),
                ('features', [feature.to_dict() for feature in self._features])])

    @property
    def id_field(self):
        return self._id_field

    @property
    def instance_generator(self):
        return self._instance_generator

    @property
    def blackout_seconds(self):
        """ Number of seconds before a prediction event to drop from training. """
        return self._blackout_seconds

    @property
    def negative_fraction(self):
        """ Fraction of 0-label instances to include in training. """
        return self._negative_fraction

    @property
    def timestamp_field(self):
        return self._timestamp_field

    @property
    def features(self):
        return self._features

    def get_feature_width(self):
        # Add one for "non of the above"
        return sum([len(x._categories) + 1 for x in self._features])

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

class DictionaryRowExtractor(object):
    def __init__(self, field_name):
        self._field_name = field_name
        self._splits = field_name.split(".")
     
    def _extract(self, row, index):        
        if index == len(self._splits):
            return row
        if self._splits[index] in row:
            value = row[self._splits[index]]
            if type(value) in (tuple, list):
                results = []
                for entry in value:
                    result = self._extract(entry, index + 1)
                    if result is not None:
                        if type(result) is list:
                            results.extend(result)
                        else:
                            results.append(result)
                return results if len(results) > 0 else None
            else:
                return self._extract(value, index + 1)

    def extract(self, row):
        if len(self._splits) == 1:
            return row[self._field_name]
        else:
           return self._extract(row, 0)

    def get_fields(self):
        return [self._field_name]

class ModelConfigRowHandler(object):
    def __init__(self, model_config, csv_input=False, counter = None):
        self._counter = counter

        self._model_config = model_config
        generator_package_name, generator_name = model_config.instance_generator.rsplit(".", 1)
        package = importlib.import_module(generator_package_name)
        self._instance_generator = getattr(package, generator_name)()
        self._csv_input = csv_input
        self._buckets = []
        self._id_extractor = DictionaryRowExtractor(model_config.id_field)
        for feature in model_config.features:
            # TODO(chris): Support non-categorical
            if feature.categories:
                self._buckets.append(SimpleCategoricalBucket(feature.field, DictionaryRowExtractor(feature.field), feature.categories))
            else:
                self._buckets.append(ValueBucket(feature.field, DictionaryRowExtractor(feature.field), has_null = True))


    def get_fields(self):
        fields = []
        for bucket in self._buckets:
            fields.extend(bucket._extractor.get_fields())
        fields.append(self._model_config.timestamp_field)
        # Label and id will get added elsewhere.
        return fields

    def replace_field_names_with_index(self, cursor):
        # Instead of using a DictCursor, use a regular cursor,
        # and rewrite the extractor field names with array
        # offsets.  This speeds up data loading by about 20%.
        header = [x.name for x in cursor.description]
        self.replace_field_names_with_index_header(header)

    def replace_field_names_with_index_header(self, header):
        for bucket in self._buckets:
            bucket._extractor.update_fields_by_id(header)

    def get_id_from_row(self, row):
        return row[self._model_config.id_field]

    def add_sequence_examples(self, row_iterator, writer):
        # Restore this each time since global state is not saved in Beam
        set_counter_impl(self._counter)

        dup_count = 0
        output_prediction_instances = []
        # Make sure we have a list, and not an iterator.
        rows = list(row_iterator)
        # Sort rows by timestamp.  We skipped doing this in SQL-land to make time to first by fast.
        rows = sorted(rows, key=lambda row: row[self._model_config.timestamp_field])
        new_rows = []
        bucket_data = []
        dup_count = 0
        # Remove duplicates
        for row in rows:
            duplicate = True
            data = self.make_feature_dictionary(row)
            data['timestamp'] = timestamp_to_epoch(row[self._model_config.timestamp_field])
            if len(bucket_data) == 0:
                duplicate = False
            else:
                last_data = bucket_data[-1]
                if (data['timestamp'] - last_data['timestamp']) > self._model_config._dup_max_time:
                    duplicate = False
                else:
                    for k in data:
                        if k != 'timestamp' and data[k] != last_data[k]:
                            duplicate = False
                            break
            if not duplicate:                    
                bucket_data.append(data)
                new_rows.append(row)
            else:
                dup_count += 1
        
        rows = new_rows
        # Make downsampling deterministic.
        rng = random.Random()
        rng.seed(self.get_id_from_row(rows[0]))
        prediction_instances = self._instance_generator.get_instances(rows)

        # Don't give a user more than 100 training instances.  Just use the last 100.
        # This number is more tuned for minimizing mapreduce stragglers than anything else.
        # With the current dataset this affects about 0.35% (.0035) of users.
        # TODO(chris): Do we still need this?
        if len(prediction_instances) > 100:
            prediction_instances = prediction_instances[-100:]

        # Add a training instance for each prediction event, including all events up to that event.
        instance_count = 0
        positive_instance_count = 0
                  
        for instance_i, instance in enumerate(prediction_instances):
            # Downsample negative examples if needed.
            if instance.label == False and rng.random() >= self._model_config.negative_fraction:
                continue

            end_index = instance.end - 1
            # Get the context_page_path from the prediction event.
            prediction_context_page_path = rows[end_index]['context_page_path']

            # Limit data to the prediction event minus the blackout period.
            last_usable_event_index = end_index
            while last_usable_event_index >= 0 and self._elapsed(rows[last_usable_event_index], rows[end_index]) < self._model_config.blackout_seconds:
                last_usable_event_index -= 1
                if last_usable_event_index < 0:
                    return 0, 0, output_prediction_instances, rows

            # Create the example

            entry = self.make_sequence_example(
                rows[instance.begin:(last_usable_event_index + 1)], bucket_data[instance.begin:(last_usable_event_index + 1)],
                instance, prediction_context_page_path, '%s_%d' % (self.get_id_from_row(rows[0]), end_index))
            output_prediction_instances.append(PredictionInstance(
                instance.begin, last_usable_event_index + 1, instance.label, final_dwell = None, future_data = instance.future_data))

            writer.write(entry.SerializeToString())
            instance_count += 1
            positive_instance_count += (instance.label == True)

        # TODO(jjs) - remove everything but output_prediction_instances
        return instance_count, positive_instance_count, output_prediction_instances, rows

    def make_feature_dictionary(self, row):
        output = {}
        for bucket in self._buckets:
            value = bucket.bucketize(row)
            output[bucket._name] = value

        return output
        
    def make_sequence_example(self, rows, bucket_data, instance, prediction_context_page_path, instance_id):
        context = tf.train.Features(feature={
            'future_data' : tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[str(instance.future_data if instance.future_data else "")])),
            'id': tf.train.Feature(bytes_list=tf.train.BytesList(value=[instance_id.encode('utf-8')])),
            'label': ModelConfigRowHandler._int64_feature(instance.label if instance.label is not None else 99)})


        feature_values = {'categorical': []}
        width = self._model_config.get_feature_width()
        for row, row_bucket_data in zip(rows, bucket_data):
            offset = 0
            indicies = [0] * width
            # Join all feature buckets into 1 feature which has all features.
            # The output is basically the set of all indicies in the output vector that should
            # be turned on.

            for bucket in self._buckets:
                value = row_bucket_data[bucket._name]
                for entry in value:
                    # Add one to account for -1 "NONE" value
                    indicies[offset + entry + 1] = 1

                offset += len(bucket._category_value_map) + 1

            feature_values['categorical'].append(tf.train.Feature(int64_list=tf.train.Int64List(value=indicies)))

        # Add time before next event.
        # row_epochs = [timestamp_to_epoch(row[self._model_config.timestamp_field]) for row in rows]
        # TODO(chris): Move this out into a feature type in ModelConfig?
        feature_values['dwell'] = []
        for i in range(len(rows) - 1):
            delta = bucket_data[i + 1]['timestamp'] - bucket_data[i]['timestamp']
            feature_values['dwell'].append(feature_coding.compute_dwell_feature(delta))

        feature_values['dwell'].append(feature_coding.compute_dwell_feature(instance.final_dwell))

        # Add current_item
        feature_values['current_cpp'] = []
        for row in rows:
            context_page_path = row['context_page_path']
            if context_page_path == '':
                feature = [0, 0, 1]
            elif context_page_path == prediction_context_page_path:
                feature = [1, 0, 0]
            else:
                feature = [0, 1, 0]
            feature_values['current_cpp'].append(tf.train.Feature(int64_list=tf.train.Int64List(value=feature)))

        # Telescoping is an attenuation feature [N, T] = Dropped N events and T seconds after this event.
        # Currently: If we have more than E (20) events, keep the first one, the last E-1, and telescope the rest.
        TELESCOPE_TO_LENGTH = self._model_config._max_events
        feature_values['telescope'] = [tf.train.Feature(int64_list=tf.train.Int64List(value=[0, 0])) for i in range(min(len(rows), TELESCOPE_TO_LENGTH))]
        if len(rows) > TELESCOPE_TO_LENGTH:
            # First cut out events
            for feature in list(feature_values.keys()):
                feature_values[feature] = [feature_values[feature][0]] + feature_values[feature][-(TELESCOPE_TO_LENGTH-1):]

            # Then set the telescope feature on the first event.
            feature_values['telescope'][0] = tf.train.Feature(int64_list=tf.train.Int64List(value=[len(rows) - TELESCOPE_TO_LENGTH, bucket_data[-(TELESCOPE_TO_LENGTH-1)]['timestamp'] - bucket_data[1]['timestamp']]))

        # Example code for adding a time_to_move feature.
        # Don't forget to also uncomment the corresponding lines in dataset_pipeline.py.
        #
        # feature_values['time_to_move'] = []
        # for row in rows:
        #     if row['event'] == 'quiz_step' and row['move_in_date']:
        #         timestamp = datetime.datetime.strptime(row['timestamp'][:19], '%Y-%m-%d %H:%M:%S')
        #         move_in_date = datetime.datetime.strptime(row['move_in_date'][:19], '%Y-%m-%d %H:%M:%S')
        #         time_until_move = move_in_date - timestamp
        #         feature = [time_until_move.days, 0]
        #     else:
        #         feature = [0, 1]
        #    feature_values['time_to_move'].append(tf.train.Feature(int64_list=tf.train.Int64List(value=feature)))

        feature_lists = tf.train.FeatureLists(feature_list={k: tf.train.FeatureList(feature=v) for k, v in list(feature_values.items())})

        return tf.train.SequenceExample(context=context, feature_lists=feature_lists)

    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    def _elapsed(self, first_row, second_row):
        second_timestamp = second_row[self._model_config.timestamp_field]
        first_timestamp = first_row[self._model_config.timestamp_field]
        if self._csv_input:
            first_timestamp = timestamp_to_epoch(first_timestamp)
            second_timestamp = timestamp_to_epoch(second_timestamp)
        return second_timestamp - first_timestamp
