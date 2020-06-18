import datetime
import logging
import petl
import re
import requests
import time

from parsons import Table
from parsons.utilities import check_env
from parsons.utilities.api_connector import APIConnector

logger = logging.getLogger(__name__)


class RTVFailure(Exception):
    """Exception raised when there is an error with the connector."""


class RockTheVote:
    REQUEST_HEADERS = {
        # For some reason, RTV's firewall REALLY doesn't like the
        # user-agent string that Python's request library gives by default,
        # though it seems fine with the curl user agent
        # For more info on user agents, see:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        'user-agent': 'curl/7.54.0'
    }

    def __init__(self, partner_id=None, partner_api_key=None):
        self.partner_id = check_env.check('RTV_PARTNER_ID', partner_id)
        self.partner_api_key = check_env.check('RTV_PARTNER_API_KEY', partner_api_key)

        self.client = APIConnector(self.uri)

    def list_registrations(self, registrations_since=None, existing_report_id=None,
                           report_timeout_seconds=3600):
        report_url = 'https://vr.rockthevote.com/api/v4/registrant_reports.json'
        if not existing_report_id:
            # Create the report for the new data
            credentials = {
                'partner_id': self.partner_id,
                'partner_API_key': self.partner_api_key,
            }

            report_parameters = credentials.copy()

            if registrations_since:
                report_parameters['since'] = registrations_since.isoformat()

            # The report parameters get passed into the request as JSON in the body
            # of the request.
            response = self.client.request(report_url, json=report_parameters)
            if response.status_code != requests.codes.ok:
                raise RTVFailure("Couldn't create RTV registrations report")

            response_json = response.json()

            # The status URL will tell us how to check the status of the report.
            status_url = response_json.get('status_url')

            # The download URL tells us where to get the report. If it's not set,
            # then the report isn't ready and we need to wait
            download_url = response_json.get('download_url')
        else:
            status_url = f'https://vr.rockthevote.com/api/v4/registrant_reports/{existing_report_id}'
            download_url = None

        # If we didn't get a status_url and we didn't get a download_url back
        # in the JSON response, then something went really wrong and we can't do
        # anything
        if not status_url and not download_url:
            raise RTVFailure("Couldn't create RTV report")

        # Let's figure out at what time should we just give up because we waited
        # too long
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=report_timeout_seconds)

        # If we have a download URL, we can move on and just download the
        # report. Otherwise, as long as we haven't run out of time, we will
        # check the status.
        while not download_url and datetime.datetime.now() < end_time:
            logger.info(f'Registrations report not ready yet, sleeping 60 seconds')

            # We just got the status, so we should wait a minute before
            # we check it again.
            time.sleep(60)

            # Check the status again via the status endpoint
            logger.info(f'Checking report status at: {status_url}')
            status_response = requests.get(
                status_url, params=credentials, headers=self.REQUEST_HEADERS)

            # Check to make sure the call got a valid response
            if status_response.status_code == requests.codes.ok:
                status_json = status_response.json()

                # Grab the download_url from the response.
                download_url = status_json.get('download_url')
            else:
                raise RTVFailure("Couldn't get report status")

        # If we never got a valid download_url, then we timed out waiting for
        # the report to generate. We will log an error and exit.
        if not download_url:
            raise RTVFailure('Timed out waiting for report')

        # Download the report data
        download_response = requests.get(
            download_url, params=credentials, headers=self.REQUEST_HEADERS)

        # Check to make sure the call got a valid response
        if download_response.status_code == requests.codes.ok:
            report_data = download_response.text

            # Load the report data into a Parsons Table
            table = Table.from_csv_string(report_data)

            # Transform the data from the report's CSV format to something more
            # Pythonic
            normalized_column_names = [
                re.sub(r'\s', '_', name)
                for name in table.columns
            ]
            normalized_column_names = [
                re.sub(r'[^A-Za-z\d_]', '', name)
                for name in normalized_column_names
            ]
            table.table = petl.setheader(table.table, normalized_column_names)
            return table
        else:
            raise RTVFailure('Unable to download report data')
