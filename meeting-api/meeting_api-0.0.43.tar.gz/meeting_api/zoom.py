import requests
import time
import base64
import hashlib
import hmac


def get_signature(api_key, api_secret, meeting_number, role, **kwargs):
    ts = int(round(time.time() * 1000)) - 30000
    msg = api_key + str(meeting_number) + str(ts) + str(role)
    message = base64.b64encode(bytes(msg, 'utf-8'))
    secret = bytes(api_secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    hash = base64.b64encode(hash.digest())
    hash = hash.decode("utf-8")
    tmpString = "%s.%s.%s.%s.%s" % (
        api_key, str(meeting_number), str(ts),
        str(role), hash)
    signature = base64.b64encode(bytes(tmpString, "utf-8"))
    signature = signature.decode("utf-8")
    signature = signature.rstrip("=")

    return signature


class Zoom:
    def __init__(self, access_token):
        self.access_token = access_token
        self.message = None
        self.users = None
        self.user = None
        self.meeting = None

    def __get_users(self):
        url = 'https://api.zoom.us/v2/users/'
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        rq = requests.get(url=url, headers=headers)

        json = rq.json()
        if 'code' in json.keys():
            self.errors = {'code': 0, 'message': json['message']}
            return False
        else:
            self.users = json['users']
            return True

    def create_user(self, email, first_name, last_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        json = {
            'action': 'create',
            'user_info': {
                'email': email,
                'type': 1,
                'first_name': first_name,
                'last_name': last_name
            }
        }
        url = 'https://api.zoom.us/v2/users/'

        rq = requests.post(url=url, headers=headers, json=json)

        json = rq.json()
        if 'code' in json.keys():
            self.errors = json
            return False
        else:
            self.user = json

        return True

    def check_user_exist(self, email=None, account_id=None):
        """Check zoom user is exist. If true, update user attribute of object

        Args:
            email (string): Email of user need to be create zoom user

        Returns:
            [Boolean]: Return true if user is exists. Else False.
        """
        if email is not None or account_id is not None:
            get_users_success = self.__get_users()
            if get_users_success is True:
                # update user is true if zoom user is exists
                is_existed = False

                if email:
                    for user in self.users:
                        if user['email'] == email:
                            self.user = user
                            is_existed = True
                    return is_existed
                elif account_id:
                    for user in self.users:
                        if user['id'] == account_id:
                            self.user = user
                            is_existed = True

                return is_existed
            else:
                return False

    def create_meeting(
            self, schedule_for, **kwargs):
        """Send request to zoom system to create meeting

        Args:
            schedule_for (string): email to assign host of zoom meeting
            first_name (str, optional): First name of host.
            last_name (str, optional): Last name of host.
            topic (str, optional): Topic of meeting.

        Returns:
            True|False: True if creating succeed. Else False.
        """
        if self.check_user_exist(schedule_for) is False:
            message = 'User with this email is not exists.'
            self.errors = {'code': 1, 'message': message}
            return False

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        json = kwargs

        url = 'https://api.zoom.us/v2/users/{}/meetings'.format(
            self.user['id'])

        rq = requests.post(url, headers=headers, json=json)
        json = rq.json()
        if 'code' in json.keys():
            self.errors = {'code': 0, 'message': json['message']}
            return False
        else:
            self.meeting = json
            return True

    def delete_meeting(self, meeting_id):
        url = 'https://api.zoom.us/v2/meetings/{}'
        url = url.format(meeting_id)

        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

        response = requests.delete(url=url, headers=headers)
        json = response.json()
        if 'code' in json.keys():
            self.errors = {'code': 0, 'message': json['message']}
            return False
        else:
            return True
