from models.page_object_models import CinescopeRegisterPage, CinescopeLoginPage
from utils.data_generator import DataGenerator

import time
import pytest
import allure
from playwright.sync_api import Page


@allure.epic("Тестирование UI")
@allure.feature("Регистрация")
@pytest.mark.ui
class TestRegistrationPage:
	@allure.title("Хэппи-пасс тест регистрации нового пользователя через UI")
	def test_register_with_ui(self, page: Page):
		"""Тест регистрации нового пользователя через UI."""

		# Генерация случайных данных пользователя
		full_name = DataGenerator.generate_random_name()
		email = DataGenerator.generate_random_email()
		password = DataGenerator.generate_random_password()

		register_page = CinescopeRegisterPage(page)

		register_page.register(
			full_name,
			email,
			password,
			password
		)

		# Ожидание перенаправления на главную страницу
		register_page.assert_was_redirect_to_login_page()

		# Скриншот страницы и прикрепление к отчету
		register_page.make_screenshot_and_attach_to_allure()

		# Проверка аллерта
		register_page.assert_alert_was_pop_up()

		#time.sleep(5)

@allure.epic("Тестирование UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLoginPage:
	@allure.title("Хэппи-пасс тест авторизации пользователя через UI")
	def test_login_with_ui(self, page: Page, registered_user):
		login_page = CinescopeLoginPage(page)

		login_page.login(registered_user.email, registered_user.password)

		login_page.assert_was_redirect_to_home_page()

		# Скриншот страницы и прикрепление к отчету
		login_page.make_screenshot_and_attach_to_allure()

		login_page.assert_alert_was_pop_up()

		#time.sleep(3)
