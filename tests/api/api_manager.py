from tests.api.auth_api import AuthAPI
from tests.api.user_api import UserAPI
from requests import Session


class ApiManager:
	"""
	Класс для управления API-классами с единой HTTP-сессией.
	"""
	def __init__(self, session: Session):
		self._session = session
		self.auth_api = AuthAPI(session)
		self.user_api = UserAPI(session)
