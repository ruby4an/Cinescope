import json
import logging
import os
from requests import Session
from pydantic import BaseModel
from constants.constants import RED, GREEN, RESET


class CustomRequester:
	"""
	Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
	"""
	base_headers = {
		"Content-Type": "application/json",
		"Accept": "application/json"
	}

	def __init__(self, session: Session, base_url):
		"""
		Инициализация кастомного реквестера.
		:param session: Объект requests.Session.
		:param base_url: Базовый URL API.
		"""
		self._session = session
		self._base_url = base_url
		self._headers = self.base_headers.copy()
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)

	@property
	def headers(self):
		return self._headers

	@property
	def session(self):
		return self._session

	def send_request(self, method, endpoint, params: dict = None, data=None, expected_status=200, need_logging=True):
		"""
		Универсальный метод для отправки запросов.
		:param params: параметры запроса (query)
		:param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
		:param endpoint: Эндпоинт (например, "/login").
		:param data: Тело запроса (JSON-данные).
		:param expected_status: Ожидаемый статус-код (по умолчанию 200).
		:param need_logging: Флаг для логирования (по умолчанию True).
		:return: Объект ответа requests.Response.
		"""
		url = f"{self._base_url}{endpoint}"

		if isinstance(data, BaseModel):
			data = json.loads(data.model_dump_json(exclude_unset=True))

		response = self._session.request(method, url, json=data, params=params)

		if need_logging:
			self.log_request_and_response(response)

		if response.status_code != expected_status:
			raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")

		return response

	def update_session_headers(self, **kwargs):
		"""
		Обновление заголовков сессии.
		:param kwargs: Дополнительные заголовки.
		"""
		self._headers.update(kwargs)
		self._session.headers.update(self._headers)

	def log_request_and_response(self, response):
		"""
		Логирование запросов и ответов. Настройки логирования описаны в pytest.ini
		Преобразует вывод в curl-like (-H хэдеры), (-d тело)

		:param response: Объект response получаемый из метода "send_request"
		"""
		try:
			request = response.request
			headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
			full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

			body = ""
			if hasattr(request, 'body') and request.body is not None:
				if isinstance(request.body, bytes):
					body = request.body.decode('utf-8')
				elif isinstance(request.body, str):
					body = request.body
				body = f"-d '{body}' \n" if body != '{}' else ''

			self.logger.info(
				f"{GREEN}{full_test_name}{RESET}\n"
				f"curl -X {request.method} '{request.url}' \\\n"
				f"{headers} \\\n"
				f"{body}"
			)

			response_status = response.status_code
			is_success = response.ok
			response_data = response.text
			if not is_success:
				self.logger.info(f"\tRESPONSE:"
								 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
								 f"\nDATA: {RED}{response_data}{RESET}")
		except Exception as e:
			self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")

