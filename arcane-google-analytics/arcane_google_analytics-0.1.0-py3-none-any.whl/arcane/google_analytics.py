import json
import logging
from typing import Dict, List

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from arcane.core.exceptions import BadRequestError


def get_metrics_from_view(ga_view: str,
                          adscale_key: str,
                          date_ranges: Dict=None,
                          metrics: List=None,
                          **optional_params):
    """
    helper to call the Google Analytics Core Reporting API. More information on the following link :
    https://developers.google.com/analytics/devguides/reporting/core/v4/basics
    """

    if metrics is None:
        metrics = [{'expression': 'ga:transactions'}]
    if date_ranges is None:
        date_ranges = [{'startDate': '30daysAgo', 'endDate': 'yesterday'}]

    required_params = {
        'viewId': ga_view,
        'dateRanges': date_ranges,
        'metrics': metrics
        }

    body = {'reportRequests': [{**required_params, **optional_params}]}

    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = service_account.Credentials.from_service_account_file(adscale_key, scopes=scopes)

    service = build('analyticsreporting', 'v4', credentials=credentials)

    try:
        res = service.reports().batchGet(body=body).execute()
    except HttpError as err:
        message = json.loads(err.content).get('error').get('message')
        raise BadRequestError(f'Error while getting data from GA. "{message}"') from err
    logging.info(res)
    return res
