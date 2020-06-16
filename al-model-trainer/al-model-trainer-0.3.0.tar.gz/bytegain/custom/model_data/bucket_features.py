class FeatureBucketerLinear(object):
    """
    feature_list: TableInfo object
    excluded_features: list
    """
    def __init__(self, excluded_features, feature_list):
        self._excluded_features = set(excluded_features)
        self._features = feature_list
        self._buckets = {}
        self._counts = {'categorical': 0, 'numerical': 0, 'boolean': 0, 'time': 0, 'excluded': 0}
        self._feature_map = {}
        self._total_length = 0
        self._num_buckets = [17, 20] # [Numerical buckets without inf and None, Total number of numerical buckets]

    @property
    def total_length(self):
        return self._total_length

    @property
    def feature_map(self):
        return self._feature_map

    def construct_buckets(self):
        """
        Construct buckets for all features based on the schema from TableInfo file

        Bucketing logic: Each feature is encoded into a one-hot vector. All one-hots are concatenated together into a
        large sparse vector

        Assumption: there are only 4 data types: character - categorical, boolean, time-like and numerical

        How does it work?
        1) "construct_buckets" stage:
        - For each feature we construct two maps: one-hot encoding map and feature index map

        One hot encoding map:
         - e.g. boolean features are associated with the following map
         `bucketer._buckets['boolean_feature'] = {'f': 0, 't': 1, '': 2, None: 2}`
         - Map's width is determined either by the nature of the feature (e.g. boolean features always
         have width 3) or is set by a user (e.g. for numerical features we choose the bucket width)

        Feature index map:
         - Each feature gets its position in the final output vector, "feature index"
            {feature1, feature2, ..., featureN} ->  {index1, index2, ..., indexN}

        2) "sample_to_vec" stage:
         - One-hot and feature maps are combined to form one large sparse vector, which encodes all features
         {feature_1, feature_2, ..., feature_N} - > [one_hot_1, one_hot_2, ..., one_hot_N] = output
        :return:
        """

        bucket_index = 0
        for col in self._features.columns:
            print("Feature: %s" % col)
            if col.name in self._excluded_features:
                self._counts['excluded'] += 1
                continue
            # Categorical features
            if 'character' in col.datatype:
                buckets = self.category_buckets(sorted(col._groups, key=lambda x: x[1]))
                self._buckets[col.name] = buckets
                bucket_len = len(buckets)
                self._counts['categorical'] += 1
            # Boolean features
            elif col.datatype == 'boolean':
                # Treat None or '' as a separate state
                self._buckets[col.name] = {'f': 0, 't': 1, '': 2, None: 2}
                bucket_len = 4
                self._counts['boolean'] += 1
            # Time-like features - ignore them
            elif 'time' in col.datatype:
                # Add time-like features into excluded set
                self._excluded_features.add(col.name)
                bucket_len = 0
                self._counts['time'] += 1
                continue
            # Numerical features
            else:
                stats = col.median, col.percentile_25, col.percentile_75
                buckets = self.numerical_buckets(stats)
                self._buckets[col.name] = buckets
                bucket_len = self._num_buckets[1]
                self._counts['numerical'] += 1
            self._feature_map[col.name] = bucket_index
            bucket_index += bucket_len
        self._total_length = bucket_index
        print("Bucketed features: %d, total number of features: %d" % (len(self._buckets), len(self._features.columns)))
        print("Length of buckets: %d" % self._total_length)
        # Print features used
        print("Features used")
        print("=========================================================")
        for k, v in list(self._buckets.items()):
            print("Feature: %s, value: %s" % (k, v))
        # return len(self._buckets)

    def category_buckets(self, groups):
        """
        Buckets for categorical features
        :param groups:
        :return:
        """
        # Category -> index map
        cat_ind_map = {}
        for index, (name, fraction) in enumerate(groups):
            # Map `None` to ''
            if not name:
                name = ''
            cat_ind_map[name] = index
        # Treat None or '' as a separate state
        if '' not in cat_ind_map:
            index += 1
            cat_ind_map[''] = index
        index += 1
        cat_ind_map['other'] = index
        return cat_ind_map

    def numerical_buckets(self, stats):
        """
        Buckets for numerical features
        :param stats:
        :param num_buckets:
        :return:
        """
        import numpy as np
        (median, perc25, perc75) = stats
        bins = np.linspace(perc25, perc75, self._num_buckets[0])
        bins = np.insert(bins, 0, -np.inf)
        bins = np.append(bins, np.inf)
        return bins

    def sample_to_vec(self, sample):
        """
        Encode features into one large sparse vector
        :param sample:
        :return: sparse vector
        """
        import logging
        import numpy as np
        sample_vec = [0]*self._total_length
        bucketed_features = set([])
        all_features = set([])
        total_length = 0
        for k, v in list(sample.items()):
            all_features.add(k)
            if k in self._excluded_features:
                continue
            # print 'Feature: %s' % k
            bucket_map = self._buckets.get(k, [])
            if len(bucket_map)<1:
                continue
            index0 = self._feature_map[k]
            # Categorical and bool features
            if isinstance(bucket_map, dict):
                v = '' if v is None else v
                index = index0 + bucket_map.get(v)
                bucket_len = len(bucket_map)
                if index is None:
                    logging.info("Index None for feature :%s, value %s, bucket map %s" % (k, v, bucket_map))
            else:
                # print 'Numerical bucket length %d' % len(bucket_map)
                # Treat None as a separate state
                bucket_len = len(bucket_map) + 1
                if v == '':
                    index = index0 + bucket_len - 1
                # Other numerical
                else:
                    index = index0 + np.digitize(float(v), bucket_map) - 1
            total_length += bucket_len
            # print 'Feature %s, bucket length %d' % (k, bucket_len)
            if bucket_len > 0:
                sample_vec[index] = 1
                bucketed_features.add(k)
        # print 'Total Length %d' % total_length
        return sample_vec


class FeatureBucketerNonLinear(FeatureBucketerLinear):
    """
    Inherits from FeatureBucketerLinear and overrides numerical feature binning
    """
    def __init__(self, excluded_features, feature_list, n_numerical_buckets=10):
        super(FeatureBucketerNonLinear, self).__init__(excluded_features, feature_list)
        self._num_buckets = [n_numerical_buckets - 1, n_numerical_buckets]  # Reserve one bucket for None

    def numerical_buckets(self, stats):
        """
        Buckets for numerical features
        :param stats: statistics extracted during data generation
        :param num_buckets:
        :return:
        """
        beta, alpha = 0.8, 0.2
        import numpy as np
        (median, perc25, perc75) = stats
        b = np.log((1/alpha - 1)/(1/beta - 1)) / (perc75 - perc25)
        a = np.exp(b * perc25) * (1 / alpha - 1)
        bins = np.linspace(0, 1, self._num_buckets[0])
        # print 'a: %s, b: %s' % (a, b)
        return a, b, bins

    def sample_to_vec(self, sample):
        """
        Encode features into one large sparse vector
        :param sample:
        :return:
        """
        import logging
        import numpy as np
        # Sparse output feature vector
        sample_vec = [0] * self._total_length
        # For stats
        bucketed_features = set([])
        all_features = set([])
        total_length = 0
        # Set a bit for each feature
        for k, v in list(sample.items()):
            all_features.add(k)
            if k in self._excluded_features:
                continue
            # print 'Feature: %s' % k
            # Get on-hot map
            bucket_map = self._buckets.get(k, [])
            if len(bucket_map) < 1:
                continue
            # Get feature index
            index_feature = self._feature_map[k]
            if index_feature is None:
                logging.error("Feature bucket index is None for feature: %s, value: %s, "
                              "bucket map: %s" % (k, v, bucket_map))
            # Categorical and boolean features
            if isinstance(bucket_map, dict):
                v = '' if v is None else v
                # Compute index within the bucket
                index_cur = bucket_map.get(v) if v in bucket_map else bucket_map.get('other')
                if index_cur is None:
                    logging.error("Feature index within bucket is None for feature: %s, value: %s, "
                                  "bucket map: %s, sample: %s" % (k, v, bucket_map, sample))
                index = index_feature + index_cur
                bucket_len = len(bucket_map)
            # Numerical features
            else:
                bucket_len = len(bucket_map[2]) + 1  # bucket_map returns `(a, b, bins)`, we need only bins
                # Treat None as a separate state
                if v == '':
                    index = index_feature + bucket_len - 1
                # Other numerical values
                else:
                    a, b, bins = bucket_map
                    func = 1 / (1 + a * np.exp(- b * float(v)))
                    index = index_feature + np.digitize(func, bins) - 1
            total_length += bucket_len
            # print 'Feature %s, bucket length %d' % (k, bucket_len)
            if bucket_len > 0:
                sample_vec[index] = 1
                bucketed_features.add(k)
        # print 'Total Length %d' % total_length
        return sample_vec


class FeatureBucketerDirect(FeatureBucketerLinear):
    def __init__(self, excluded_features, feature_list):
        super(FeatureBucketerDirect, self).__init__(excluded_features, feature_list)

    # Construct buckets for all features based on TableInfo
    def construct_buckets(self):
        # Assume that there are only 4 data types: character - categorical, boolean, time-like and numerical
        total_length = 0
        for col in self._features.columns:
            if col.name in self._excluded_features:
                self._counts['excluded'] += 1
                continue
            print('Feature: %s' %col.name)
            if 'character' in col.datatype:
                buckets = self.category_buckets(sorted(col._groups, key=lambda x: x[1]))
                self._buckets[col.name] = buckets
                bucket_len = len(buckets)
                self._counts['categorical'] += 1
            elif col.datatype == 'boolean':
                # Treat None or '' as a separate state
                self._buckets[col.name] = {'f': 0, 't': 1, '': 2, None: 2}
                bucket_len = 4
                self._counts['boolean'] += 1
            elif 'time' in col.datatype:
                self._counts['time'] += 1
                # Add time-like features into excluded set
                self._excluded_features.add(col.name)
                bucket_len = 0
            else:
                self._counts['numerical'] += 1
                self._buckets[col.name] = [0, 0]
                bucket_len = 2
            total_length += bucket_len
            # print 'Feature %s, bucket length %d' % (col.name, bucket_len)
        print(("Bucketed features: %d, total # of features: %d, excluded: %d " % (
        len(self._buckets), len(self._features.columns), len(self._excluded_features))))
        print("# of buckets: %d" % total_length)
        # Print features used
        print("Features used")
        print("=========================================================")
        for k, v in list(self._buckets.items()):
            print("Feature: %s, value: %s" % (k, v))
            # return len(self._buckets)

    # Bucket features
    def sample_to_vec(self, sample):
        import logging
        import numpy as np
        sample_vec = []
        bucketed_features = set([])
        all_features = set([])
        total_length = 0
        for k, v in list(sample.items()):
            all_features.add(k)
            if k in self._excluded_features:
                continue
            # print 'Feature: %s' % k
            bucket_map = self._buckets.get(k, [])
            if len(bucket_map) < 1:
                continue
            # Categorical and bool features
            if isinstance(bucket_map, dict):
                v = '' if v is None else v
                index = bucket_map.get(v)
                bucket_len = len(bucket_map)
                if index is None:
                    logging.info("Index None for feature :%s, value %s, bucket map %s" % (k, v, bucket_map))
                vec = [0] * bucket_len
                vec[index] = 1
            else:
                bucket_len = 2
                vec = [0] * bucket_len
                if v == '':
                    vec[0] = 1
                # Other numerical
                else:
                    vec[1] = float(v)
            bucketed_features.add(k)
            sample_vec += vec
            total_length += bucket_len
        return sample_vec
