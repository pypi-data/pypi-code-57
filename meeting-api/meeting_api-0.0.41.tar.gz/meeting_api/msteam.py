import requests


class ApplicationAccessToken:
    def __init__(self, tenant_id, client_id, client_secret):
        self.data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'tenant_id': tenant_id,
            'scope': '.default'}

        # generate and save url to get access_token
        self.generate_url()
        # update access token to self
        self.update()

    def generate_url(self):
        url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'
        self.url = url.format(self.data['tenant_id'])

    def update(self):
        response = requests.post(url=self.url, data=self.data)

        data = response.json()
        if 'error' in data.keys():
            self.token = None
            self.errors = data['error_description']
        else:
            self.token = data['access_token']


class ApplicationTeam:
    def __init__(self, tenant_id, client_id, client_secret, **kwargs):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        # update access token
        self.update_access_token()

    def update_access_token(self):
        self.access_token = ApplicationAccessToken(
            self.tenant_id, self.client_id, self.client_secret)

        if not self.access_token.token:
            self.errors = (self.access_token.errors)

    def check_user_exists(self, email):
        """Check team user is exists or not

        Returns:
            [bool]: True if user is exists, else False.
        """

        url = 'https://graph.microsoft.com/v1.0/users'
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token.token)}

        response = requests.get(url=url, headers=headers)
        data = response.json()

        for user in data['value']:
            if user['userPrincipalName'] == email:
                return True
        return False

    def is_valid(self):
        if not hasattr(self, 'errors'):
            return True
        else:
            return False

    def check(self):
        if not hasattr(self, 'access_token'):
            self.update_access_token()

    def create_user(
            self, displayName, mailNickname, userPrincipalName,
            password, **kwargs):
        self.check()

        data = {
            'accountEnabled': True,
            'displayName': displayName,
            'mailNickname': mailNickname,
            'userPrincipalName': userPrincipalName,
            'passwordProfile': {
                'forceChangePasswordNextSignIn': True,
                'password': password}}

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token.token),
            'content-type': 'application/json'}

        response = requests.post(
            'https://graph.microsoft.com/v1.0/users', json=data,
            headers=headers)
        json = response.json()
        if 'error' in json.keys():
            self.errors = json['error']['message']
            return False
        else:
            self.user = json
            return True


class DelegatedAccessToken(ApplicationAccessToken):
    def __init__(self, code, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data.update({
            'code': code, 'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'})

    def generate_url(self):
        url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'
        url = url.format(self.data['tenant_id'])
        return url


class DelegatedTeam(ApplicationAccessToken):
    def generate_get_code_url(self, redirect_uri, state):
        data = {
            'redirect_uri': redirect_uri, 'state': state,
            'response_type': 'code', 'client_id': self.client_id,
            'scope': '.default', 'state': state}

        url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/authorize?'
        url = url.format(data['tenant_id'])

        for key in self.data.keys():
            if not url.endswith('?'):
                url = url + '&'
            url = url + '{}={}'.format(key, data[key])

        return url

    def update_access_token(self):
        self.access_token = DelegatedAccessToken(
            self.code, self.tenant_id, self.redirect_uri, self.client_id,
            self.client_secret)
        self.access_token.update()

        if not self.access_token.token:
            self.errors = self.access_token.errors

    def create_meeting(self, start_time, end_time, subject):
        self.check()

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token.token),
            'content-type': 'application/json'}

        data = {
            'startDateTime': start_time,
            'endDateTime': end_time,
            'subject': subject}
        if hasattr(self, 'user'):
            data.update({
                'participants': {'organizer': {'identity': {'user': {
                    'id': self.user.userid}}}}})

        response = requests.post(
            url='https://graph.microsoft.com/v1.0/me/onlineMeetings',
            headers=headers, json=data)
        return_values = response.json()

        if 'error' in return_values.keys():
            self.errors = return_values['error']['message']
            return False
        else:
            self.meeting_url = return_values['joinUrl']
            return True
