from netauto._exceptions import FailedToLogin


class Auth:

    def __init__(self, session, username, password):
        self._session = session
        self._username = username
        self._password = password

    def login(self) -> None:
        user_data = {"username": self._username, "password": self._password}
        r = self._session.post(url="auth", data=user_data)
        if r.status_code != 201:
            raise FailedToLogin(r.text)
        else:
            access_token = r.json()["access_token"]
            self._session.headers["Authorization"] = f"Bearer {access_token}"
            return None
