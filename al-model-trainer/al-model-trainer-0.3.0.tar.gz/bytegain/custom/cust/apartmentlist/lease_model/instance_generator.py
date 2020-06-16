from bytegain.zap.prediction_instance import PredictionInstance
from bytegain.custom.cust.apartmentlist.user_value_model.instance_generator import RentInstanceGenerator

DAY_SECONDS = 24 * 3600


class LeaseInstanceGenerator(RentInstanceGenerator):
    def get_instances(self, rows):
        """
        Predict if a user will sign a lease at a given property.

        Label is extracted from features as follows: label = extra_features.get('leased_at_property') == 't'
        One training example per set of features.
        Use up to 7 days of data after the label.

        :param rows: list[dict], a user session
        :return: instances: list[PredictionInstance]
        """
        if len(rows) == 0:
            return []

        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp

        # Find all sets of features
        all_extra_features = [row for row in rows if row.get('type') == 'features']
        get_counter('instance', 'features_found').inc(len(all_extra_features))

        get_counter('instance', 'users').inc()

        instances = []

        # Make sure the number of feature buckets is the same
        default_buckets = [0] * self._bucketer.total_length

        # Predict mode - use the most recent features and construct one instance without a length limit
        if self._predict_mode:
            extra_features_buckets = default_buckets
            label = False
            if all_extra_features:
                extra_features = all_extra_features[-1]
                extra_features_buckets = self._bucketer.sample_to_vec(extra_features)
                label = extra_features.get('leased_at_property') == 't'
            # We don't need to look for the last page event, rows_filter will do it later
            if not label:
                instances.append(PredictionInstance(0, len(rows), label, predict_index=None, final_dwell=None,
                                                    future_data=None, extra_features=extra_features_buckets))
                get_counter('instance_generator', 'instance_generated').inc()
        else:
            latest_page_i = None
            # In training mode make instance per set of features
            if all_extra_features:
                features_i = 0
                timestamp_features = timestamp_to_epoch(get_timestamp(all_extra_features[features_i]))
                for row_i, row in enumerate(rows):
                    if row.get('type') == 'page':
                        latest_page_i = row_i
                    timestamp_row = timestamp_to_epoch(get_timestamp(rows[row_i]))
                    # Generate instance using up to 1 week of data after the label
                    if (timestamp_row - timestamp_features > 7 * DAY_SECONDS or row_i == len(rows) - 1) and latest_page_i:
                        label = all_extra_features[features_i].get('leased_at_property') == 't'
                        extra_features_buckets = self._bucketer.sample_to_vec(all_extra_features[features_i])
                        instances.append(PredictionInstance(0, latest_page_i + 1, label, predict_index=None, final_dwell=None,
                                                            future_data=None, extra_features=extra_features_buckets))
                        # Now use the next set of features
                        features_i += 1
                        if features_i == len(all_extra_features):
                            break
                        else:
                            timestamp_features = timestamp_to_epoch(get_timestamp(all_extra_features[features_i]))
        return instances


class LeaseInstanceGeneratorAfterFeatures(RentInstanceGenerator):
    def get_instances(self, rows):
        """
        NOTE: PREDICT MODE IS NOT IMPLEMENTED!

        Predict if a user will sign a lease at a given property.

        Label is extracted from features as follows: label = extra_features.get('leased_at_property') == 't'
        One training example per set of features.
        Use up to 7 days of data after the label.

        :param rows: list[dict], a user session
        :return: instances: list[PredictionInstance]
        """
        from bytegain.beam.beam_util import get_counter

        instances = []
        # Create instances only at the following events
        instance_events = {'page', 'screen', 'compass'}

        # Make sure the number of feature buckets is the same
        default_buckets = [0] * self._bucketer.total_length

        extra_features = {}
        for row_i, row in enumerate(rows):
            event_type = row.get('type')
            if event_type == 'compass':
                same_property = row.get('rental_id') == extra_features.get('rental_id')
                rows[row_i]['same_property'] = same_property
                get_counter('instance_generator', 'same_property_%s' % same_property).inc()
            if event_type == 'features':
                extra_features = row
                label = extra_features.get('leased_at_property') == 't'
                extra_features_buckets = self._bucketer.sample_to_vec(extra_features)
                get_counter('instance', 'features_found').inc()
                instance_begin = row_i
                instance_end = self.find_instance_end(rows=rows, rows_start=row_i,
                                                      days=7, instance_events=instance_events)
                if instance_end:
                    instances.append(PredictionInstance(instance_begin, instance_end + 1, label,
                                                        predict_index=None, final_dwell=None,
                                                        future_data=None, extra_features=extra_features_buckets))

        get_counter('instance', 'users').inc()

        # TODO (yuri): Implement predict mode if needed

        # # Predict mode - use the most recent features and construct one instance without a length limit
        # if self._predict_mode:
        #     extra_features_buckets = default_buckets
        #     label = False
        #     if all_extra_features:
        #         extra_features = all_extra_features[-1]
        #         extra_features_buckets = self._bucketer.sample_to_vec(extra_features)
        #         label = extra_features.get('leased_at_property') == 't'
        #     # We don't need to look for the last page event, rows_filter will do it later
        #     if not label:
        #         instances = [PredictionInstance(0, len(rows), label, predict_index=None, final_dwell=None,
        #                                             future_data=None, extra_features=extra_features_buckets)]
        #         get_counter('instance_generator', 'instance_generated').inc()
        return instances

    @staticmethod
    def find_instance_end(rows, rows_start, days, instance_events):
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp

        latest_instance_page = None
        instance_end = None
        timestamp_features = timestamp_to_epoch(get_timestamp(rows[rows_start]))
        for row_i in range(rows_start + 1, len(rows)):
            if (timestamp_to_epoch(get_timestamp(rows[row_i])) - timestamp_features >
                        days * DAY_SECONDS or row_i == len(rows) - 1) and latest_instance_page:
                instance_end = latest_instance_page
                break
            if rows[row_i].get('type') in instance_events:
                latest_instance_page = row_i
        return instance_end
