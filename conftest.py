from typing import Generator
from faker import Faker
import pytest
import requests
import time
from sqlalchemy.orm import Session
from constants.constants import AUTH_BASE_URL, REGISTER_ENDPOINT
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from models.base_models import TestUser
from resourses.user_creds import SuperAdminCreds
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from entities.user import User
from constants.roles import Roles
#from utils.front_tools import Tools

faker = Faker()
DEFAULT_UI_TIMEOUT = 30000  # 30 seconds


@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    def _internal() -> TestUser:
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


@pytest.fixture(scope="function")
def registered_user(requester, test_user, db_helper):
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
    user_id = registered_user.id = response_data["id"]
    yield registered_user
    # teardown
    if db_helper.get_user_by_id(user_id):
        db_helper.delete_user_by_id(user_id)
    assert db_helper.get_user_by_id(user_id) is None, "Не удалился"


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
        roles=[Roles.SUPER_ADMIN],
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
        [Roles.ADMIN],
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
        [Roles.USER],
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
        updated_data.passwordRepeat=None
        return updated_data
    return _internal

@pytest.fixture(scope="module")
def db_session()-> Generator[Session, None, None]:
    db_session = get_db_session()
    try:
        yield db_session
    finally:
        db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    try:
        yield user
    # Cleanup
    finally:
        if db_helper.get_user_by_id(user.id):
            db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper):
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    try:
        yield movie
    # Cleanup
    finally:
        if db_helper.get_movie_by_id(movie.id):
            db_helper.cleanup_test_data([movie])
            assert db_helper.get_movie_by_id(movie.id) is None, f"Фильм с ID '{movie.id}' не был удален из базы"

@pytest.fixture(scope="function")
def created_ebnutiy_movie(db_helper):
    ebnutaya_data = DataGenerator.generate_movie_data()
    ebnutaya_data['name'] = "Ебнутая комедия игорь подзалупный"
    movie = db_helper.create_test_movie(ebnutaya_data)
    try:
        yield movie
    # Cleanup
    finally:
        if db_helper.get_movie_by_id(movie.id):
            db_helper.cleanup_test_data([movie])
            assert db_helper.get_movie_by_id(movie.id) is None, f"Фильм с ID '{movie.id}' не был удален из базы"

@pytest.fixture
def delay_between_retries():
    time.sleep(2)
    yield

#----------------- Playwright fixtures ----------------#

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    # ----- Закомментировал трейсинг чтобы не плодить мусор в файлах -----
    #log_name = f"trace_{Tools.timestamp()}.zip"
    #trace_path = Tools.files_dir('playwright_trace', log_name)
    #context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

