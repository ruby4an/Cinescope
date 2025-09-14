from faker import Faker
import pytest
import requests
from constants.constants import AUTH_BASE_URL, REGISTER_ENDPOINT
from models.base_models import TestUser
from resourses.user_creds import SuperAdminCreds
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from entities.user import User
from constants.roles import Roles

faker = Faker()


@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    def _internal():
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        data =  {
            "email": random_email,
            "fullName": random_name,
            "password": random_password,
            "passwordRepeat": random_password,
            "roles": [Roles.USER.value]
        }
        return TestUser(**data)
    return _internal


@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    data = test_user()
    response_data = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=data,
        expected_status=201
    ).json()
    registered_user = data
    registered_user.id = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_BASE_URL)


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


@pytest.fixture(scope="session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="session")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        email=SuperAdminCreds.USERNAME,
        password=SuperAdminCreds.PASSWORD,
        roles=[Roles.SUPER_ADMIN.value],
        api=new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="session")
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()
    data = creation_user_data()

    admin = User(
        data.email,
        data.password,
        [Roles.ADMIN.value],
        new_session
    )

    user_id = super_admin.api.user_api.create_user(data).json()["id"]

    patch_data = {
        "roles": [Roles.ADMIN.value]
    }

    super_admin.api.user_api.edit_user(user_id, patch_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture(scope="session")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    data = creation_user_data()

    common_user = User(
        data.email,
        data.password,
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="session")
def creation_user_data(test_user):
    def _internal():
        updated_data = test_user()
        updated_data.verified=True
        updated_data.banned=False
        return updated_data
    return _internal
