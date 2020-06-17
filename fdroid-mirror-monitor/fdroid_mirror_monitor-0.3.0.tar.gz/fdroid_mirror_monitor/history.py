#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor.utils import get_logger

# stdlibs
from datetime import datetime, timezone
import json
import requests
import statistics


class History:
    '''
    History
    '''
    log = get_logger(__name__)

    def __init__(self, url=None, timeout=60):
        self.url = url
        if url is not None:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            # convert timestamp string to int
            self.history = response.json(object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
        else:
            self.history = {}

    def save(self, path):
        '''
        Save history as JSON

        :param path: filepath
        '''
        with open(path, 'w') as fp:
            json.dump(self.history, fp)

    def add(self, status, timestamp):
        '''
        Append status to history

        :param status: dict
        :param timestamp: (int/str) save status in history under this timestamp
        '''

        self.history[timestamp] = status

    def trim(self, hours):
        '''
        delete timestamps older than x hours

        :param hours: number of hours from now to the past
        :return: number of timestamps after trimming
        '''
        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        border = current_timestamp - (60*60*hours)

        for timestamp in list(self.history.keys()):
            if int(timestamp) < border:
                del self.history[timestamp]

    def historical_status(self, hours):
        '''
        summarize history per mirror and calculate the average values of the last x hours
        and return as complete status dict

        :param hours: number of hours from now to the past
        :return: status dict
        '''

        ts_relevant = []
        ts_24h = []

        current_ts = int(datetime.now(timezone.utc).timestamp())
        border_relevant = current_ts - (60*60*hours)
        border_24h = current_ts - (60*60*24)

        for timestamp in list(self.history.keys()):
            ts = timestamp
            if ts >= border_relevant:
                # relevant
                ts_relevant.append(timestamp)

            if ts >= border_24h:
                ts_24h.append(timestamp)

        # latest first
        ts_relevant.sort(reverse=True)
        status = self.history[ts_relevant[0]]

        # if there is just one timestamp skip calculations
        if len(ts_relevant) == 1:
            return status

        ts_24h.sort(reverse=True)
        check_period = ts_24h[0] - ts_24h[-1]
        status['num_checks_24h'] = len(ts_24h)

        if check_period > 0:
            secs = check_period // (len(ts_24h)-1)
            hours = secs // 3600
            minutes = (secs % 3600) // 60
            status['check_rate_24h'] = '%02d:%02d' % (hours, minutes)
        else:
            status['check_rate_24h'] = None

        for mirror in status['mirrors']:
            name = mirror['name']
            durations = []
            historical = {}
            latest_ts = None
            errors = []
            delays = []

            for ts in ts_relevant:
                for historical_mirror in self.history[ts]['mirrors']:
                    # calculate average duration and standard deviation
                    if historical_mirror['name'] == name:
                        if latest_ts is None:
                            latest_ts = ts
                        elif ts > latest_ts:
                            self.log.warning('unsorted history')

                        # for detailed info
                        dt = datetime.fromtimestamp(ts, timezone.utc)
                        t_str = dt.strftime('%F %T')
                        historical[t_str] = {}

                        for d in ['duration', 'success', 'errors']:
                            try:
                                historical[t_str][d] = historical_mirror[d]
                            except KeyError:
                                pass

                        try:
                            modified_str = historical_mirror['index']['modified']
                            historical[t_str]['modified'] = modified_str.replace(' UTC', '')
                        except KeyError:
                            pass
                        else:
                            # delay
                            modified_dt = datetime.strptime(modified_str, '%Y-%m-%d %H:%M:%S UTC')
                            t_dt = datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
                            timedelta = t_dt - modified_dt
                            seconds = timedelta.total_seconds()
                            if seconds <= 0:
                                self.log.warning('negative timedelta. modified: %s timestamp: %s' % (modified_str, t_str))
                                seconds = 0

                            delays.append(seconds)

                            hours = seconds // 3600
                            minutes = (seconds % 3600) // 60
                            historical[t_str]['delay'] = '%d:%02d' % (hours, minutes)

                        for d in ['check_ip', 'check_country', 'check_country_code']:
                            historical[t_str][d] = self.history[ts][d]

                        # for additional processing
                        if ts in ts_24h:
                            for err in historical_mirror['errors']:
                                if err != {}:
                                    errors.append((t_str, historical_mirror['errors'][err]))

                        if 'duration' in historical_mirror:
                            durations.append(historical_mirror['duration'])

            # error summary
            def main_err_latest(main_err):
                for t_str in historical:
                    for err in historical[t_str]['errors']:
                        if historical[t_str]['errors'][err] == main_err:
                            return t_str

            main_err_count = 0
            if len(errors) > 0:
                errors = sorted(errors, reverse=True)
                error_msgs = list(map(list, zip(*errors)))[1]
                main_err = statistics.mode(error_msgs)
                mirror['main_err_msg'] = main_err
                mirror['main_err_count'] = main_err_count = error_msgs.count(main_err)
                for err in errors:
                    if err[1] == main_err:
                        mirror['main_err_latest'] = err[0]
                        break

            # average duration
            if len(durations) > 0:
                median = statistics.median(durations)
                mean = statistics.fmean(durations)
                #  σ² / Var(duration)
                variance = statistics.pvariance(durations, mean)

                mirror['duration'] = round(mean, 2)
                mirror['duration_median'] = round(median, 2)
                mirror['duration_variance'] = round(variance, 2)

            # average delay
            if len(delays) > 0:
                mean = statistics.fmean(delays)
                secs = int(mean)
                hours = secs // 3600
                minutes = (secs % 3600) // 60
                mirror['delay'] = '%d:%02d' % (hours, minutes)
                delay_f = secs / 3600

            # mirror score
            try:
                score = mirror['duration'] + mirror['duration_variance'] + main_err_count + delay_f
                mirror['score'] = round(score, 2)
            except KeyError:
                pass

            mirror['historical'] = historical

        return status
