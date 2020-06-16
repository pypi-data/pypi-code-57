import argparse
import os
import datetime
from bytegain.nn_tools.verify_past_predictions import  verify_predictions
import bytegain.custom.data_import.db_utils as db_utils
import bytegain.data_import.segment_utils as segment_utils


def get_outcomes(start_date, predictions):

    src_conn_factory = db_utils.ConnectionFactory(os.environ['AL_REDSHIFT_URL'])
    cur = src_conn_factory.get_connection().cursor()

    select = """
select user_id from etl.acappella_leases 
where created_at > %(date)s order by 1"""
    cur.execute(select, {'date': start_date})

    outcomes = {}
    for k in list(predictions.keys()):
        outcomes[k] = 0
    positives = 0
    for row in cur:
        user_id = str(row[0])
        if user_id in predictions:
            outcomes[user_id] = 1
            positives += 1

    return outcomes, positives


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Takes predictions made in the past and verifies them using new data.")
    parser.add_argument('--prediction_made_date', type = segment_utils.as_date,
                        required=True, help='Date when predictions_where made')
    args = parser.parse_args()
    previous_week = args.prediction_made_date -datetime.timedelta(days=7)
    path = "gs://bg-dataflow/apartmentlist/user_value/predictions/{start_date}-{end_date}/AL_user_value_predictions_{start_date}-{end_date}.json"
    path = path.format(start_date=previous_week.date().isoformat(), end_date=args.prediction_made_date.date().isoformat())
    verify_predictions(path, lambda predictions: get_outcomes(args.prediction_made_date, predictions))



