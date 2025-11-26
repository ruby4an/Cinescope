from api.api_manager import ApiManager
from pydantic import EmailStr


class User:
    def __init__(self, email: str | EmailStr, password: str, roles: list, api: ApiManager):
        self._email = email
        self._password = password
        self._roles = roles
        self._api = api

    @property
    def creds(self) -> tuple:
        return self._email, self._password

    @property
    def api(self) -> ApiManager:
        return self._api

    @property
    def email(self) -> str:
        return self._email