import datetime
import logging

from bytegain.custom.model_data.model_config import get_epoch_times_for_rows
from bytegain.zap.prediction_instance import PredictionInstance, increment_counter

MINUTE = datetime.timedelta(minutes=1)

def row_is_modal_view(row):
    return 'event' in row and row['event'] == 'modals' and row['name'] == 'signup' and row['action'] == 'view'


def row_is_sign_up(row):
    return 'event' in row and row['event'] in ('user_signed_up', 'social_sign_in')

def row_is_logged_in(row):
    return 'event' in row and row['event'] in ('user_logged_in', 'user_social_login')

def row_is_interest(row):
    return 'event' in row and row['event'] == 'cycle_choice'

def row_is_positive_interest(row):
    return row_is_interest(row) and row['action'] in ('maybe', 'love-it', 'email', 'go-visit')

def row_is_notification(row):
    return 'event' in row and row['event'] == 'interest' and (
           'leased_at_notified_property' in row and row['leased_at_notified_property'] in ('t', 'f'))


class LoginInstanceGenerator(object):
    """ Instance generator for Apartmentlist's signup modal.

    Positive instances take one of two forms:
    1) modals name=signup action=view -> modals name=signup action=submit -> user_signed_up
    2) modals name=signup action=view -> modals name=signup action=email_taken -> social_sign_in

    """
    def get_instances(self, rows):
        epoch_times = get_epoch_times_for_rows(rows)

        # Generate a prediction event for each login modal view.
        instances = []
        for trigger_i, trigger_row in enumerate(rows):
            # Don't generate any instances after the user's first login.
            if row_is_logged_in(trigger_row):
                increment_counter('users_with_login')
                break

            if row_is_modal_view(trigger_row):
                # Label is whether they logged in in the next 10 minutes.
                logged_in = False
                for i in range(trigger_i + 1, len(rows)):
                    time_since_trigger = epoch_times[i] - epoch_times[trigger_i]
                    if time_since_trigger > 10*MINUTE:
                        break
                    if row_is_sign_up(rows[i]):
                        increment_counter('signin-%s' % rows[i]['event'])
                        logged_in = True
                        break
                instances.append(PredictionInstance(0, trigger_i, logged_in))
                break

        return instances


class ModalBounceInstanceGenerator(object):
    """ Instance generator whether showing Apartmentlist's signup modal will cause a bounce.

    Negative instances take one of three forms:
    1) modals name=signup action=view -> modals name=signup action=submit -> user_signed_up
    2) modals name=signup action=view -> modals name=signup action=email_taken -> social_sign_in
    3) Still on site after 5min

    Positive instances look like this:
    1) modals name=signup action=view -> everything else

    """
    def get_instances(self, rows):
        epoch_times = get_epoch_times_for_rows(rows)

        # Generate a prediction event for each login modal view.
        instances = []
        for trigger_i, trigger_row in enumerate(rows):
            # Don't generate any instances after the user's first login.
            if row_is_logged_in(trigger_row):
                increment_counter('users_with_login')
                break

            if row_is_modal_view(trigger_row):
                bounce = True
                for i in range(trigger_i + 1, len(rows)):
                    if row_is_sign_up(rows[i]):
                        increment_counter('xbounce-signup')
                        bounce = False
                        break
                    seconds_since_trigger = epoch_times[i] - epoch_times[trigger_i]
                    if seconds_since_trigger > 5*MINUTE and seconds_since_trigger < 60*MINUTE:
                        increment_counter('xbounce-activity')
                        bounce = False
                        break

                instances.append(PredictionInstance(0, trigger_i, bounce))
                break

        return instances

class AbandonInstanceGenerator(object):
    """ Instance generator for Apartmentlist's cycling matches UI.

    Positive instances are where user continued to look at more matches

    """
    def get_instances(self, rows):
        positive = False
        instances = []
        # Find the last positive interest
        last = 0
        interests = 0
        for i, row in enumerate(rows):
            if row_is_positive_interest(row):
                interests += 1
                last = min(i + 1, len(rows) - 1)

        total_notifications = AbandonInstanceGenerator.count_notifications(rows[0:last + 1])
        increment_counter("Notifications for user %2d" % total_notifications)
        increment_counter("Total positive interests", interests)
        increment_counter("Total notifications", total_notifications)

        for trigger_i, trigger_row in enumerate(rows):
            if not positive or row_is_positive_interest(trigger_row):
                positive = True

            if positive and row_is_positive_interest(trigger_row):
                notifications = AbandonInstanceGenerator.count_notifications(rows[trigger_i + 1: last + 1])
                future_data = "%d %d" % (total_notifications, notifications)
                increment_counter("Future_Data: %s" % future_data)
                outcome = False
                for i in range(trigger_i + 1, len(rows)):
                    if row_is_positive_interest(rows[i]):

                        instances.append(PredictionInstance(
                            0, trigger_i + 1, True, i, future_data =future_data))
                        outcome = True
                        break
                if not outcome:
                    instances.append(PredictionInstance(
                        0, trigger_i + 1, False, future_data =future_data))
        return instances

    @staticmethod
    def count_notifications(rows):
        count = 0
        for row in rows:
            if row_is_notification(row):
                count +=1
        return count
def filter_view_button(event):
    return 'event' not in event or event['event'] != 'buttons' or event['action'] != 'view'