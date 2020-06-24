from django.conf import settings
from psu_base.classes.Log import Log
from psu_base.classes.Faki import Faki
from psu_base.services import message_service
import requests
import json

log = Log()


class Finti:
    token = None
    finti_url = None
    auth = None
    content_type = {'Content-Type': 'application/json'}
    reduce_logging = False
    suppress_logging = False

    # For caching finti responses for offline development
    # This should only be used for local development
    faki = None
    simulate = None
    simulate_when_possible = None
    prepare_offline = None

    # Calls with regular/registered Finti tokens
    def get(self, path, parameters=None, include_metadata=False):
        """
        Get a response from Finti
        :param path:             Finti path relative to root Finti URL
        :param parameters:       Object (map) of parameters to send to Finti
        :param include_metadata: Include status, version, result, jwt?              (default: False)
        """
        params = {'path': path, 'parameters': parameters}
        if not self.suppress_logging:
            log.trace(params)

        json_response = None

        # If simulating responses, or preparing to simulate them in the future, prepare a Faki instance
        if self.simulate or self.prepare_offline or self.simulate_when_possible:
            self.faki = Faki(
                path, method='GET', parameters=parameters, payload=None, headers=None
            )

        # If getting offline data
        simulated = False
        if self.simulate or self.simulate_when_possible:
            try:
                json_response = self.faki.retrieve()
                simulated = "No data found" not in json_response
            except Exception as ee:
                message_service.post_error(f"Error retrieving Faki data: {str(ee)}")

        # Otherwise, get real Finti data
        # If not simulating, or if simulation attempt failed
        is_simulating = self.simulate or self.simulate_when_possible
        must_simulate = self.simulate and not self.simulate_when_possible
        if is_simulating and (simulated or must_simulate):
            if not self.suppress_logging:
                log.debug("Using simulated response")
        else:
            try:
                params = parameters if parameters else {}
                api_url = self.get_url(path)
                if not (self.suppress_logging or self.reduce_logging):
                    log.info("Calling {0}".format(api_url))
                response = requests.get(
                    api_url, params=params, auth=self.auth, verify=False,
                    hooks={'response': self.handle_response}
                )
                json_response = response.text

                # If saving response data for later offline use
                if self.prepare_offline:
                    self.faki.save(json_response)
            except Exception as ee:
                if not self.suppress_logging:
                    log.error(f"Error retrieving Finti data: {str(ee)}")

        # Convert the JSON string into data
        response_data = json.loads(json_response) if json_response else None

        result = None
        if include_metadata:
            result = response_data

        elif response_data and 'message' in response_data:
            result = response_data['message']

        if not (self.suppress_logging or self.reduce_logging):
            log.end(type(result))
        return result

    def delete(self, path, parameters=None, include_metadata=False):
        """
        Make a DELETE call on Finti API
        :param path:             Finti path relative to root Finti URL
        :param parameters:       Object (map) of parameters to send to Finti
        :param include_metadata: Include status, version, result, jwt?              (default: False)

        Note: If using offline simulation, objects will not be removed, you'll just get a simulated successful response
        """
        params = {'path': path, 'parameters': parameters}
        if not self.suppress_logging:
            log.trace(params)

        json_response = None

        # If simulating responses, or preparing to simulate them in the future, prepare a Faki instance
        if self.simulate or self.prepare_offline:
            self.faki = Faki(
                path, method='DELETE', parameters=parameters, payload=None, headers=None
            )

        # If getting offline data
        if self.simulate:
            try:
                json_response = self.faki.retrieve()
            except Exception as ee:
                message_service.post_error(f"Error retrieving Faki data: {str(ee)}")

        # Otherwise, get real Finti data
        else:
            try:
                params = parameters if parameters else {}
                api_url = self.get_url(path)
                if not (self.suppress_logging or self.reduce_logging):
                    log.info("Calling {0}".format(api_url))

                response = requests.delete(
                    api_url, params=params, auth=self.auth, verify=False,
                    hooks={'response': self.handle_response}
                )
                json_response = response.text

                # If saving response data for later offline use
                if self.prepare_offline:
                    self.faki.save(json_response)

            except Exception as ee:
                if not self.suppress_logging:
                    log.error("Finti DELETE error: {}".format(ee))

        # Convert the JSON string into data
        response_data = json.loads(json_response) if json_response else None

        result = None
        if include_metadata:
            result = response_data

        elif response_data and 'message' in response_data:
            result = response_data['message']

        if not (self.suppress_logging or self.reduce_logging):
            log.end(type(result))
        return result

    def post(self, path, payload=None, parameters=None, headers=None, include_metadata=False):
        params = {'path': path, 'parameters': parameters}
        if not self.suppress_logging:
            log.trace(params)

        json_response = None

        # If simulating responses, or preparing to simulate them in the future, prepare a Faki instance
        if self.simulate or self.prepare_offline:
            self.faki = Faki(
                path, method='POST', parameters=parameters, payload=payload, headers=headers
            )

        # If getting offline data
        if self.simulate:
            try:
                json_response = self.faki.retrieve()
            except Exception as ee:
                message_service.post_error(f"Error retrieving Faki data: {str(ee)}")

        # Otherwise, get real Finti data
        else:
            try:
                params = parameters if parameters else {}
                api_url = self.get_url(path)
                headers = self.check_content_header(headers if headers else {})
                if not (self.suppress_logging or self.reduce_logging):
                    log.info("Calling {0}".format(api_url))

                response = requests.post(
                    api_url, data=payload if payload else {}, headers=headers, auth=self.auth, verify=False,
                    hooks={'response': self.handle_response}
                )
                json_response = response.text

                # If saving response data for later offline use
                if self.prepare_offline:
                    self.faki.save(json_response)
            except Exception as ee:
                if not self.suppress_logging:
                    log.error("Finti POST error: {}".format(ee))

        # Convert the JSON string into data
        response_data = json.loads(json_response) if json_response else None

        result = None
        if include_metadata:
            result = response_data

        elif response_data and 'message' in response_data:
            result = response_data['message']

        if not (self.suppress_logging or self.reduce_logging):
            log.end(type(result))
        return result

    def put(self, path, payload=None, parameters=None, headers=None, include_metadata=False):
        params = {'path': path, 'parameters': parameters}
        if not self.suppress_logging:
            log.trace(params)

        json_response = None

        # If simulating responses, or preparing to simulate them in the future, prepare a Faki instance
        if self.simulate or self.prepare_offline:
            self.faki = Faki(
                path, method='PUT', parameters=parameters, payload=payload, headers=headers
            )

        # If getting offline data
        if self.simulate:
            try:
                json_response = self.faki.retrieve()
            except Exception as ee:
                message_service.post_error(f"Error retrieving Faki data: {str(ee)}")

        # Otherwise, get real Finti data
        else:
            try:
                params = parameters if parameters else {}
                api_url = self.get_url(path)
                headers = self.check_content_header(headers if headers else {})
                if not (self.suppress_logging or self.reduce_logging):
                    log.info("Calling {0}".format(api_url))

                response = requests.put(
                    api_url, data=payload if payload else {}, headers=headers, auth=self.auth, verify=False,
                    hooks={'response': self.handle_response}
                )
                json_response = response.text

                # If saving response data for later offline use, and a successful response was received
                if self.prepare_offline and json_response and 'success' in json_response:
                    self.faki.save(json_response)
            except Exception as ee:
                if not self.suppress_logging:
                    log.error("Finti PUT error: {}".format(ee))

        # Convert the JSON string into data
        response_data = json.loads(json_response) if json_response else None

        result = None
        if include_metadata:
            result = response_data

        elif response_data and 'message' in response_data:
            result = response_data['message']

        if not (self.suppress_logging or self.reduce_logging):
            log.end(type(result))
        return result

    @staticmethod
    def handle_response(response, *args, **kwargs):
        """No need to call this directly. This is called via the get method"""
        wdt_response = {
            'status': '',
            'result': '',
            'version': None,
            'jwt': None,
            'message': ''}
        try:
            wdt_response['status'] = response.status_code

            # Some responses have json-able content, some don't

            if response.status_code == requests.codes.OK:
                try:
                    response_data = response.json()

                    wdt_response['result'] = 'success'

                    # Check if response structure is the same as wdt_response
                    if type(response_data) in [list, str] or len(set(wdt_response.keys()).difference(set(response_data.keys()))) > 0:
                        wdt_response['message'] = response_data
                    else:
                        return response
                except Exception as ex:
                    response_data = response.text
                    wdt_response['result'] = 'error'
                    wdt_response['message'] = response.text
                    log.error('Status code was OK, but response is not JSON: {}'.format(ex))

            elif response.status_code == requests.codes.NOT_FOUND:
                response_data = response.json()
                wdt_response['result'] = 'not_found'

                # Check if response structure is the same as wdt_response
                if type(response_data) == str or len(set(wdt_response.keys()).difference(set(response_data.keys()))) > 0:
                    wdt_response['message'] =  response_data
                else:
                    return response

            else:
                log.error("API Unsuccessful:\n{0}".format(response.text))
                if response.status_code == requests.codes.FORBIDDEN:
                    wdt_response['result'] = 'forbidden'
                else:
                    wdt_response['result'] = 'error'
                message = ''
                try:
                    response_data = response.json()
                    if len(set(wdt_response.keys()).difference(set(response_data.keys()))) > 0:
                        wdt_response['message'] =  response_data
                    else:
                        return response
                    message = response_data['error']
                except Exception as ee:
                    message = response.text
                wdt_response['message'] = message

        except Exception as ee:
            log.error("Error handling Finti response: {}".format(ee))
            log.info("Finti response: {}".format(response))

        # Overwrite content with wdt_response format
        response._content = json.dumps(wdt_response).encode('utf-8')
        return response

    def get_url(self, relative_path=''):
        """No need to call this directly. This is called via the get method"""
        return f"{self.finti_url}/{relative_path}".strip('/')

    def check_content_header(self, headers):
        if any((True for ct in ['content-type', 'Content-Type'] if ct in headers.keys())):
            return headers
        return headers.update(self.content_type)

    def __init__(self, reduce_logging=False, suppress_logging=False):
        self.token = settings.FINTI_TOKEN
        self.finti_url = settings.FINTI_URL.strip('/')
        self.auth = (self.token, '')
        self.reduce_logging = reduce_logging
        self.suppress_logging = suppress_logging

        self.simulate = getattr(settings, 'FINTI_SIMULATE_CALLS', False)
        self.simulate_when_possible = getattr(settings, 'FINTI_SIMULATE_WHEN_POSSIBLE', False)
        self.prepare_offline = getattr(settings, 'FINTI_SAVE_RESPONSES', False)

