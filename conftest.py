from faker import Faker
import pytest
import requests
from constants import AUTH_BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_CRED
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from tests.api.api_manager import ApiManager

faker = Faker()


@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_BASE_URL)


@pytest.fixture(scope="session")
def admin_auth_session(requester):
    """
    Эта фикстура используется в tests\api\test_movies.py для авторизации и возвращает сессию реквестера
    """
    # Логинимся для получения токена
    login_data = {
        "username": ADMIN_CRED["username"],
        "password": ADMIN_CRED["password"]
    }
    response = requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=login_data,
        expected_status=200
    )

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    requester.update_session_headers(Autorization=f"Bearer {token}")
    return requester._session


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    try:
        yield http_session
    finally:
        http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)
