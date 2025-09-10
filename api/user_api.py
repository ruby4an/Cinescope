from custom_requester.custom_requester import CustomRequester
from constants.constants import AUTH_BASE_URL


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session, base_url=AUTH_BASE_URL)
        self._session = session

    def get_user(self, user_locator, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_locator: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def edit_user(self, user_id, new_data: dict, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"user/{user_id}",
            data=new_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"user/{user_id}",
            expected_status=expected_status
        )
