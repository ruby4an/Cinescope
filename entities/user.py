from api.api_manager import ApiManager


class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self._email = email
        self._password = password
        self._roles = roles
        self._api = api

    @property
    def creds(self):
        return self._email, self._password

    @property
    def api(self):
        return self._api

    @property
    def email(self):
        return self._email