from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse


class TestAuthApi:
	def test_register_user(self, api_manager: ApiManager, test_user):
		"""
		Тест на регистрацию пользователя.
		"""
		data = test_user().model_dump(exclude_none=True)
		response = api_manager.auth_api.register_user(data)

		register_user_response = RegisterUserResponse(**response.json())

		assert register_user_response.email == data["email"], "Email не совпадает"

	def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
		"""
		Тест на регистрацию и авторизацию пользователя.
		"""
		login_data = {
			"email": registered_user.email,
			"password": registered_user.password
		}
		response = api_manager.auth_api.login_user(login_data)
		response_data = response.json()

		assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
		assert response_data["user"]["email"] == registered_user.email, "Email не совпадает"

	def test_auth_wrong_pass(self, api_manager: ApiManager, registered_user):
		"""
		вход по левому паролю
		"""
		login_data = {
			"email": registered_user.email,
			"password": "huygavno228"
		}
		response = api_manager.auth_api.login_user(login_data, 401)

		assert response.json()["message"] != '' and response.json()["message"] is not None, "Нет сообщения об ошибке"

	def test_auth_wrong_mail(self, api_manager: ApiManager, registered_user):
		"""
		вход по левой почте
		"""
		login_data = {
			"email": "eblan228@oosd.sru",
			"password": registered_user.password
		}
		response = api_manager.auth_api.login_user(login_data, 401)

		assert response.json()["message"] != '' and response.json()["message"] is not None, "Нет сообщения об ошибке"

	def test_auth_empty(self, api_manager: ApiManager):
		"""
		вход с пустым телом запроса
		"""
		login_data = {}
		api_manager.auth_api.login_user(login_data, 401)
