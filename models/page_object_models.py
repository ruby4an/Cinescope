import os

from playwright.sync_api import Page
import allure
from typing import Literal


class PageAction:
    def __init__(self, page: Page):
        self._page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self._page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self._page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self._page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self._page.wait_for_url(url)
        assert self._page.url == url, "Редирект на домашнюю старицу не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self._page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: Literal["attached", "detached", "hidden", "visible"] = "visible"):
        self._page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self._page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)
        # Можно удалить файл скриншота после прикрепления
        os.remove(screenshot_path)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str):
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self._page.get_by_text(text)
            # Ждем появления элемента
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"


class BasePage(PageAction): #Базовая логика допустимая для всех страниц на сайте
    def __init__(self, page: Page):
        super().__init__(page)
        self._home_url = "https://dev-cinescope.coconutqa.ru/"

        # Общие локаторы для всех страниц на сайте
        self._home_button = "a[href='/' and text()='Cinescope']"
        self._all_movies_button = "a[href='/movies' and text()='Все фильмы']"
        self._submit_button = "button[type='submit']"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self._home_button)
        self.wait_redirect_for_url(self._home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self._all_movies_button)
        self.wait_redirect_for_url(f"{self._home_url}movies")


class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._url = f"{self._home_url}register"

        # Локаторы элементов
        self._full_name_input = "input[name='fullName']"
        self._email_input = "input[name='email']"
        self._password_input = "input[name='password']"
        self._repeat_password_input = "input[name='passwordRepeat']"

        self._sign_button = "a[href='/login' and text()='Войти']"

    # Локальные action методы
    def open(self):
        self.open_url(self._url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.open()
        self.enter_text_to_element(self._full_name_input, full_name)
        self.enter_text_to_element(self._email_input, email)
        self.enter_text_to_element(self._password_input, password)
        self.enter_text_to_element(self._repeat_password_input, confirm_password)

        self.click_element(self._submit_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(f"{self._home_url}login")

    def assert_alert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._url = f"{self._home_url}login"

        # Локаторы элементов
        self._email_input = "input[name='email']"
        self._password_input = "input[name='password']"

        self._register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # Локальные action методы
    def open(self):
        self.open_url(self._url)

    def login(self, email: str, password: str):
        self.open()
        self.enter_text_to_element(self._password_input, password)
        self.enter_text_to_element(self._email_input, email)
        self.click_element(self._submit_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self._home_url)

    def assert_alert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")