import requests
from constants import HEADERS, MOVIES_ENDPOINT
from utils.data_generator import DataGenerator

"""
	эТи тесты были написаны без враппера - для них нужен отдельный
"""


class TestMoviesApi:
	def test_max_lt_min(self):
		query = {
			"minPrice": 2000,
			"maxPrice": 1000
		}

		response = requests.get(MOVIES_ENDPOINT, headers=HEADERS, params=query)

		assert response.status_code == 400, "Не пришел 400 код"

	def test_create_empty_movie(self, admin_auth_session):
		body = {}

		response = admin_auth_session.post(MOVIES_ENDPOINT, headers=HEADERS, json=body)

		assert response.status_code == 400

	def test_get_film(self):
		# получаю рандомный фильм
		film = requests.get(MOVIES_ENDPOINT).json()["movies"][0]
		film_id = film["id"]
		# получаю его же по айдишнику
		response = requests.get(f"{MOVIES_ENDPOINT}/{film_id}")

		assert response.status_code == 200, "Ошибка получения фильма"
		assert response.json()["name"] == film["name"], "Имена не совпадают"

	def test_get_invalid_film(self):
		invalid_id = 22848133708

		response = requests.get(f"{MOVIES_ENDPOINT}/{invalid_id}")
		assert response.status_code == 404, "Найден фильм с несуществующим айди"

	def test_film_patch(self, admin_auth_session):
		# получаю рандомный фильм
		film = requests.get(MOVIES_ENDPOINT).json()["movies"][0]
		film_id = film["id"]

		body = {
			"name": f"{DataGenerator.generate_random_name()}",
			"price": 1488
		}

		response = admin_auth_session.patch(f"{MOVIES_ENDPOINT}/{film_id}", json=body)

		assert response.status_code == 200, "Данные не обновлены"
		assert response.json()["name"] == body["name"] and \
			response.json()["price"] == body["price"], "Данные не обновлены"
