import json
import logging
import os
from requests import Session


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
		Логирование запросов и ответов.
		:param response: Объект ответа requests.Response.
		"""
		try:
			request = response.request
			GREEN = '\033[32m'
			RED = '\033[31m'
			RESET = '\033[0m'
			headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
			full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

			body = ""
			if hasattr(request, 'body') and request.body is not None:
				if isinstance(request.body, bytes):
					body = request.body.decode('utf-8')
				body = f"-d '{body}' \n" if body != '{}' else ''

			# Логируем запрос
			self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
			self.logger.info(
				f"{GREEN}{full_test_name}{RESET}\n"
				f"curl -X {request.method} '{request.url}' \\\n"
				f"{headers} \\\n"
				f"{body}"
			)

			# Обрабатываем ответ
			response_status = response.status_code
			is_success = response.ok
			response_data = response.text

			# Попытка форматировать JSON
			try:
				response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
			except json.JSONDecodeError:
				pass  # Оставляем текст, если это не JSON

			# Логируем ответ
			self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
			if not is_success:
				self.logger.info(
					f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
					f"\tDATA: {RED}{response_data}{RESET}"
				)
			else:
				self.logger.info(
					f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
					f"\tDATA:\n{response_data}"
				)
			self.logger.info(f"{'=' * 80}\n")
		except Exception as e:
			self.logger.error(f"\nLogging failed: {type(e)} - {e}")
