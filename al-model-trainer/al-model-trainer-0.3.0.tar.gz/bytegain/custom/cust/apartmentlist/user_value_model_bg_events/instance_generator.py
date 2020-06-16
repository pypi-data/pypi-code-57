from bytegain.zap.prediction_instance import PredictionInstance
import logging
from bytegain.zap.abstract_instance_generator import InstanceGeneratorInterface
import random


def print_session_len(session_duration):
    from bytegain.beam.beam_util import get_counter
    if session_duration < 60:
        get_counter('instance_generator', 'instance_after_mins_00').inc()
    elif session_duration < 3600:
        get_counter('instance_generator',
                    'instance_after_mins_%02d_lease' % (session_duration / 60)).inc()
    elif session_duration < 3600 * 24:
        get_counter('instance_generator', 'instance_after_hrs_%02d' % (
        session_duration / 3600)).inc()
    else:
        get_counter('instance_generator', 'instance_after_days_%02d' % (
        session_duration / 3600 / 24)).inc()


def get_lease_epoch(rows):
    from bytegain.beam.beam_util import get_counter
    from bytegain.zap.abstract_instance_generator import get_timestamp, timestamp_to_epoch

    for row in rows:
        if row.get('type') == 'acappella_leases':
            get_counter('instance_generator', 'acappella_found').inc()
            return timestamp_to_epoch(get_timestamp(row))
    return None


def get_signup_timestamp(rows):
    from bytegain.zap.abstract_instance_generator import get_timestamp

    for row in rows:
        signup = row.get('context', {}).get('page', {}).get('search') == '?signup=true'
        if signup:
            return get_timestamp(row)
    return None


def get_instance_index(rows, instance_end_epoch, include_short_sessions, signup_epoch, lease_epoch, blackout_days):
    from bytegain.beam.beam_util import get_counter
    from bytegain.zap.abstract_instance_generator import get_timestamp, timestamp_to_epoch
    from bytegain.custom.cust.apartmentlist.user_value_model_bg_events.events_to_sessions import quantize

    for row_i in range(len(rows)):
        timestamp_i = timestamp_to_epoch(get_timestamp(rows[row_i]))
        # Decide if make instance even if session ends before `ending_timestamp`
        short_session = (row_i == len(rows) - 1) if include_short_sessions else False
        # Generate instance only if page event
        if rows[row_i].get('type') != 'page':
            continue
        if timestamp_i > instance_end_epoch or short_session:
            # Don't create an instance if lease after 90 days
            if lease_epoch and lease_epoch - timestamp_i > blackout_days * 24 * 3600:
                days_to_lease = (lease_epoch - timestamp_i) / 24 / 3600
                if days_to_lease > 120:
                    get_counter('instance_generator', 'lease_after_120_days').inc()
                else:
                    get_counter('instance_generator', 'lease_after_90_days').inc()
                return None
            else:
                time_since_signup_min = (timestamp_i - signup_epoch) // 60
                # if time_since_signup_min<0:
                #     # No data after sign up
                #     return None
                get_counter('instance_generator', 'time_since_signup: %06d' % quantize(time_since_signup_min)).inc()
                return row_i
    return None


class NewUserValueInstanceGenerator(InstanceGeneratorInterface):
    """
    Predict if a user will sign a lease anywhere (all acappella leases) based on some data after sign up.
    Method specifying how much data after sing up to use `get_instance_end_epoch` should be implemented
    """
    def __init__(self, ending_timestamp_func, include_short_sessions):
        self._blackout_days = 90
        self._ending_timestamp_func = ending_timestamp_func
        # Make instance even if session ends before `ending_timestamp`
        self._include_short_sessions = include_short_sessions

    def get_instances(self, rows):
        """
        :param (list[dict]) rows: a user session
        :return: (list[PredictionInstance]) instances:
        """
        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch

        instances = []

        # Find a lease event
        lease_epoch = get_lease_epoch(rows)
        label = True if lease_epoch else False

        # Ignore lease events
        rows = [row for row in rows if row.get('type') != 'acappella_leases']

        # Find if the user signed up
        signup_timestamp = get_signup_timestamp(rows)

        if signup_timestamp is None:
            return instances

        signup_epoch = timestamp_to_epoch(signup_timestamp)

        # Compute instance end time
        instance_end_epoch = self._ending_timestamp_func(signup_timestamp)
        assert instance_end_epoch > signup_epoch

        # Now generate one instance
        # Compute instance index if possible
        instance_index = get_instance_index(rows,
                                            instance_end_epoch=instance_end_epoch,
                                            include_short_sessions=self._include_short_sessions,
                                            signup_epoch=signup_epoch,
                                            lease_epoch=lease_epoch,
                                            blackout_days=self._blackout_days)
        if instance_index:
            instances.append(PredictionInstance(0, instance_index + 1, label))
        else:
            # No data after signup
            get_counter('instance_generator', 'no_data_after_signup').inc()
            # get_counter('instance_generator', 'session_no_instance_length_%04d' % len(rows_no_lease)).inc()
            # logging.info('Session: %s' % rows)
        return instances


def midnight_timestamp(signup_timestamp):
    from bytegain.zap.utils.datetime_utils import from_str
    from datetime import timedelta
    import time

    signup_dt = from_str(signup_timestamp)
    signup_dt_midnight = (signup_dt +
                          timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return time.mktime(signup_dt_midnight.timetuple())


class NewUserValueMidnightInstanceGenerator(NewUserValueInstanceGenerator):
    """
    Predict if a user will sign a lease (all acappella leases) based on only data on the day when he signed up
    """
    def __init__(self):
        super(NewUserValueMidnightInstanceGenerator, self).__init__(ending_timestamp_func=midnight_timestamp,
                                                                    include_short_sessions=True)


def first_n_minutes_timestamp(signup_timestamp, minutes=4):
    from bytegain.zap.utils.datetime_utils import from_str
    from datetime import timedelta
    import time

    signup_dt = from_str(signup_timestamp)
    signup_dt_midnight = (signup_dt + timedelta(minutes=minutes))
    return time.mktime(signup_dt_midnight.timetuple())


class NewUserValueFirstNMinutesInstanceGenerator(NewUserValueInstanceGenerator):
    """
    Predict if a user will sign a lease (all acappella leases) based on only data on the day when he signed up
    """
    def __init__(self):
        super(NewUserValueFirstNMinutesInstanceGenerator, self).__init__(
            ending_timestamp_func=first_n_minutes_timestamp, include_short_sessions=False)


class NewUserValueFirstNMinutesInstanceGeneratorOld(InstanceGeneratorInterface):
    def __init__(self):
        self._use_minutes = 4
        self._blackout_days = 120

    def get_instances(self, rows):
        """
        Predict if a user will sign a lease anywhere based on only 4 minutes of initial user data

        :param (list[dict]) rows: a user session
        :return: (list[PredictionInstance]) instances:
        """
        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp

        # Find the first lease event
        label = False
        timestamp_lease = None
        for row_i, row in enumerate(rows):
            if row.get('type') == 'acappella_leases':
                get_counter('instance_generator', 'acappella_found').inc()
                label = True
                timestamp_lease = timestamp_to_epoch(get_timestamp(row))
                break

        # Ignore lease events
        rows = [row for row in rows if row.get('type') != 'acappella_leases']

        instances = []
        timestamp_signup = None
        signup = False
        timestamp_prev = timestamp_to_epoch(get_timestamp(rows[0]))
        for row_i in range(1, len(rows)):
            timestamp_i = timestamp_to_epoch(get_timestamp(rows[row_i]))
            if timestamp_signup is not None:
                time_after_signup = timestamp_i - timestamp_signup
                # Create instance after 4 minutes since signing up.
                # NOTE: Use only users who have data after 4 minutes
                if time_after_signup > self._use_minutes * 60:
                    # Don't create an instance if lease after 90 days
                    if timestamp_lease and timestamp_lease - timestamp_i > self._blackout_days * 24 * 3600:
                        days_to_lease = (timestamp_lease - timestamp_i) / 24 / 3600
                        if days_to_lease > 120:
                            get_counter('instance_generator', 'lease_after_120_days').inc()
                        else:
                            get_counter('instance_generator', 'lease_after_90_days').inc()
                        # get_counter('instance_generator', 'lease_after_%03d_days' % days_to_lease).inc()
                    else:
                        time_since_signup_min = (timestamp_prev - timestamp_signup)//60
                        get_counter('instance_generator', 'time_since_signup: %d' % time_since_signup_min).inc()
                        # get_counter('instance_generator', 'time_since_signup_after_4_min: %05d' % ((timestamp_i -
                        #                                                              timestamp_signup)//60)).inc()
                        instances.append(PredictionInstance(0, row_i, label))
                    # One instance per user
                    break
            signup = rows[row_i].get('context', {}).get('page', {}).get('search') == '?signup=true' or signup
            # Use only first signup event
            if signup and timestamp_signup is None:
                timestamp_signup = timestamp_to_epoch(get_timestamp(rows[row_i]))
            timestamp_prev = timestamp_i
        # If haven't created an instance - no data after signup
        if len(instances) == 0:
            get_counter('instance_generator', 'no_data_after_signup').inc()
            rows_no_lease = [row for row in rows if row.get('type')!='acappella_leases']
            # get_counter('instance_generator', 'session_no_instance_length_%04d' % len(rows_no_lease)).inc()
            # logging.info('Session: %s' % rows)
        return instances


class UserValueInstanceGenerator(InstanceGeneratorInterface):
    """Based on all available data predict whether a user will sign a lease in the next X days.
    Make instances every week."""
    def __init__(self):
        lease_window_days = 90
        self._lease_window_secs = lease_window_days * 24 * 3600
        interval_days = 7
        self._interval_secs = interval_days * 24 * 3600
        random.seed(113129321)

    def config(self, driver_input, instance_generator_config, instance_config,
                                  session_generator_data, input_sessions):
        self._start_date = session_generator_data['data_start_date']
        self._end_date = session_generator_data['data_end_date']

    def get_instances(self, rows):
        """
        :param (list[dict]) rows: a user session
        :return: (list[PredictionInstance]) instances:
        """
        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp

        instances = []

        # Find the last non lease event and a lease event (if exists)
        # Ignore sessions which have lease as the first event
        last_before_lease = len(rows) - 1
        timestamp_lease = None
        for row_i, row in enumerate(rows):
            if row.get('type') == 'acappella_leases':
                if row_i == 0:
                    get_counter('instance_generator', 'lease_is_first_event').inc()
                    return instances
                get_counter('instance_generator', 'lease_found').inc()
                timestamp_lease = timestamp_to_epoch(get_timestamp(row))
                last_before_lease = row_i - 1
                break

        # Set the label
        label = False
        if timestamp_lease:
            label = True
            # If there is a big blackout between last non lease event and lease event - this is a negative example
            if timestamp_lease - timestamp_to_epoch(get_timestamp(rows[last_before_lease])) > self._lease_window_secs:
                label = False
                get_counter('instance_generator', 'lease_too_late').inc()

        # # Undersampling
        # if not label and random.randint(0, 10) != 7:
        #     get_counter('instance_generator', 'user_undersampled').inc()
        #     return instances

        # Generate instances every X days. In user is inactive generate 4 instances after he becomes inactive
        row_i = 0
        instance_timestamp = timestamp_to_epoch(get_timestamp(rows[row_i])) + self._interval_secs
        # Last date is either the timestamp of the last event before lease
        # or `end_date` that is specified to get data from BQ
        last_date = get_timestamp(rows[last_before_lease]) if timestamp_lease else self._end_date + 'T00:00:00.000000Z'
        # logging.info("Last date: %s" % last_date)
        last_timestamp = timestamp_to_epoch(last_date)
        # logging.info("Last before lease: %s" % last_before_lease)
        # Number of instances while the user is inactive
        n_instances_no_activity = 0
        while instance_timestamp <= last_timestamp:
            while row_i < last_before_lease and timestamp_to_epoch(get_timestamp(rows[row_i])) < instance_timestamp:
                # logging.info('%s' % get_timestamp(rows[row_i]))
                row_i += 1
                # logging.info("row_i: %s" % row_i)
            final_dwell = instance_timestamp - timestamp_to_epoch(get_timestamp(rows[row_i - 1]))
            instances.append(PredictionInstance(0, row_i, label, final_dwell=final_dwell))
            # logging.info('Instance created with dwell %s' % final_dwell)
            if row_i == last_before_lease:
                n_instances_no_activity += 1
            # Don't generate more than 3 instances when there is no activity
            if n_instances_no_activity > 1 and not label:
                get_counter('instance_generator', 'users_no_activity_3_weeks').inc()
                break
            instance_timestamp += self._interval_secs
        # Add instance last event
        final_dwell = instance_timestamp - timestamp_to_epoch(get_timestamp(rows[last_before_lease]))
        instances.append(PredictionInstance(0, last_before_lease + 1, label, final_dwell=final_dwell))
        # logging.info('Instance created with dwell %s' % final_dwell)
        # Test
        # sess_length_days = (last_timestamp - timestamp_to_epoch(get_timestamp(rows[0]))) / 3600 / 24
        # logging.info("Match: %s" % (sess_length_days//7 == len(instances) - 1))

        get_counter('instance_generator', 'instances_per_user_%02d' % len(instances)).inc()
        return instances

