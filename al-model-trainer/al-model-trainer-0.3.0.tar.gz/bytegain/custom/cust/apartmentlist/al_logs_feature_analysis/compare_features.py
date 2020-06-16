import argparse
import os.path

from bytegain.custom.model_data import feature_analysis

THRESHOLD = 0.05
THRESHOLD_MSG = '> %.0f%%' % (THRESHOLD * 100)
CAT_THRESHOLD = 0.1

IGNORED_FEATURES = {}


def round_if_float(v):
    if type(v) == float:
        return round(v, 4)
    return v


def approx_equal(val1, val2):
    if (val1 < 0 < val2) or (val2 < 0 < val1):
        return False
    val1 = abs(val1)
    val2 = abs(val2)
    p = abs(val1 - val2)
    if val1 > 1 or val2 > 1:
        p = p / float(max(val1, val2))
    return p <= THRESHOLD


def approx_cat_match(cat1, cat2):
    if len(cat1) != len(cat2):
        return False
    for idx, c1 in enumerate(cat1):
        c2 = cat2[idx]
        if round_if_float(c1[0]) != round_if_float(c2[0]) or abs(c1[1] - c2[1]) > CAT_THRESHOLD:
            return False
    return True


def compare_features(current_features, current_label, previous_features, previous_label):
    print('>>> Feature diff:')
    print('1st line: %s' % current_label)
    print('2nd line: %s' % previous_label)

    broken_features = []

    def add_broken_feature(feature, reason):
        broken_features.append(feature)
        print('^^^ DIFF: %s' % reason)

    previous_features_dict = {}
    for feature_info in previous_features:
        previous_features_dict[feature_info.name()] = feature_info
    for current_fi in current_features:
        previous_fi = previous_features_dict.get(current_fi.name())
        print('')
        print(current_fi)
        print(previous_fi)

        if previous_fi is None:
            add_broken_feature(current_fi.name(), 'previous data does not exist')
        elif current_fi.data_type() != previous_fi.data_type():
            add_broken_feature(current_fi.name(), 'different data types')
        elif not approx_equal(current_fi.null_fraction(), previous_fi.null_fraction()):
            add_broken_feature(current_fi.name(), 'null fraction %s' % THRESHOLD_MSG)
        elif current_fi.name() in IGNORED_FEATURES:
            continue
        elif current_fi.data_type().is_cat():
            # categorical
            previous_top_vals_dict = {}
            for val in previous_fi.top_values():
                v = round_if_float(val[0])
                previous_top_vals_dict[v] = val[1]
            for val in current_fi.top_values():
                cur_val = round_if_float(val[0])
                cur_fraction = val[1]
                prev_fraction = previous_top_vals_dict.get(cur_val, 0.0)
                if not approx_equal(cur_fraction, prev_fraction):
                    if not approx_cat_match(current_fi.top_values(), previous_fi.top_values()):
                        add_broken_feature(current_fi.name(), 'value: %s' % cur_val)
                    break
        elif current_fi.data_type().is_number():
            # non-categorical number
            if (not approx_equal(current_fi.average(), previous_fi.average()) and
                    not approx_equal(current_fi.median(), previous_fi.median())):
                add_broken_feature(current_fi.name(), 'avg and median %s' % THRESHOLD_MSG)
        else:
            # non-categorical something else -- anything to check?
            pass

    if broken_features:
        print('\n>>> Features requiring attention:\n%s' % '\n'.join(broken_features))

    return broken_features


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare feature analysis stored as local JSON files')
    parser.add_argument('request_features_file', help='Local file with request feature analysis')
    parser.add_argument('training_features_file', help='Local file with training feature analysis')
    args = parser.parse_args()
    if compare_features(feature_analysis.read_features(args.request_features_file),
                        'request logs (%s)' % os.path.basename(args.request_features_file),
                        feature_analysis.read_features(args.training_features_file),
                        'training (%s)' % os.path.basename(args.training_features_file)):
        exit(1)
