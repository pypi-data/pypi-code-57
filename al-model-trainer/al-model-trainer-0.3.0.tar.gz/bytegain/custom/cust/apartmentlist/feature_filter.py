
class FeatureFilter(object):
    def __init__(self, excluded, numerical, categorical, bucket = None):
        self._excluded = set(excluded)
        self._numerical = set(numerical)
        self._categorical = set(categorical)
        self._bucket = set(bucket)

    def create_buckets(self, features):
        buckets = []
        output_features = []
        for feature in features:
            if self.excluded(feature):
                print("Explicitly Excluding %s" % str(feature))
            elif feature.is_suitable() or self.categorical(feature):
                is_category = True if self.categorical(feature) else (False if self.numerical(feature) else None)
                is_one_hot = self.bucket(feature)
                bucket = feature.create_bucket(is_category = is_category, none_value = -2, one_hot = is_one_hot)
                buckets.append(bucket)
                output_features.append((feature, bucket))
            else:
                print("Not suitable: %s %s" % (str(feature), feature._column))

        print ("\n--------- Features -------------")
        for feature, bucket in output_features:
            print("%s  --> %s" % (feature, type(bucket)))

        return buckets

    def excluded(self, feature):
        return feature._column in self._excluded

    def numerical(self, feature):
        return feature._column in self._numerical

    def categorical(self, feature):
        return feature._column in self._categorical

    def bucket(self, feature):
        return feature._column in self._bucket
