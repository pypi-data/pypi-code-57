import json
import requests
import logging
from requests.exceptions import ConnectionError
from codewatchman.WatchmanLog import WatchmanLog

def make_cwm_request(
    endpoint,
    json_data,
    Credentials = {},
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
):
    try:
        # url = 'http://localhost:8080/v1'
        url = 'https://api.codewatchman.com/v1'
        final_url = '{}/{}'.format(url, endpoint)
        logging.info("Code Watchman URL: {}".format(final_url))
        headers["Credentials"] = json.dumps(Credentials)

        response = requests.post(
            final_url,
            json=json_data,
            headers=headers,
            timeout=10
        )
        logging.info("Request complete. {}".format(response))

        response_data = response.content.decode('utf8').replace("'", '"')
        response_json = json.loads(response_data)

        return response_json
    except ConnectionError:
        logging.debug("Code Watchman servers seems to be unavailable now")
        return { "status": "error", "message": "Server unavailable." }
    except Exception as e:
        logging.debug("Error @ Code Watchman")
        logging.exception(e)

class Watchman:
    def __init__(self, token_id, access_token):
        logging.info("Logging Id and Token: {} {}".format(token_id, access_token))
        self.token_id = token_id
        self.access_token = access_token
        self.validation_message = None

    def check_token_validity(self):
        response = make_cwm_request(
            endpoint="token/validate",
            json_data={
                "tokenId": self.token_id,
                "accessToken": self.access_token
            },
        )
        logging.debug("Checking Validity: {}".format(json.dumps(response)))
        return response


    def send_log(self, log_data):
        if type(log_data) is not WatchmanLog:
            logging.info("Use watchmanlog class to build log object")
            return
        else:
            self._sendlog(log_data)


    def _sendlog(self, log_data):
        if log_data.is_valid != True:
            logging.info("Provided log data is not valid.")

        if type(log_data.payload) is dict:
            payload = json.dumps(log_data.payload)
        else:
            payload = json.dumps({})



        response = make_cwm_request(
            endpoint="log",
            json_data={
                "message": log_data.message,
                "payload": payload,
                "logCode": log_data.log_code,
                "tokenId": self.token_id,
                "accessToken": self.access_token,
            }
        )
        logging.debug("Data logged: {}".format(json.dumps(response)))