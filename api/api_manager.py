from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI
from requests import Session


class ApiManager:
	"""
	Класс для управления API-классами с единой HTTP-сессией.
	"""
	def __init__(self, session: Session):
		self._session = session
		self.auth_api = AuthAPI(session)
		self.user_api = UserAPI(session)
		self.movies_api = MoviesAPI(session)

	def close_session(self):
		self._session.close()
