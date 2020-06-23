import requests
import os
import json


class UserManagementClient:
    WEBSERVICES_PATH = 'otrs/nph-genericinterface.pl/Webservice/UserManagement/cuser'

    @staticmethod
    def _password():
        return os.environ['OTRS_PASSW']

    @staticmethod
    def _user():
        return os.environ['OTRS_USER']

    @staticmethod
    def _url():
        return os.environ['OTRS_URL']

    @classmethod
    def set_preference(cls, key, user_id, lang):
        payload = {
            "UserLogin": cls._user(),
            "Password": cls._password(),
            "Object": "Kernel::System::CustomerUser",
            "Method": "SetPreferences",
            "Parameter": {
                "Key": key,
                "Value": lang,
                "UserID": user_id
            }
        }
        json_payload = json.dumps(payload)
        url = '{}{}'.format(cls._url(), cls.WEBSERVICES_PATH)
        requests.post(url, data=json_payload)
