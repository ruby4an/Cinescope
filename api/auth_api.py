from requests import Session
from constants.constants import REGISTER_ENDPOINT, AUTH_BASE_URL, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    """
        Класс для работы с ауе
    """

    def __init__(self, session: Session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def get_token(self, user_creds: tuple):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        return token


    def authenticate(self, user_creds: tuple):
        self.update_session_headers(**{"Authorization": "Bearer " + self.get_token(user_creds)})
