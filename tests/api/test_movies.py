from utils.data_generator import DataGenerator


class TestMoviesApi:
	def test_max_lt_min(self, super_admin):
		query = {
			"minPrice": 2000,
			"maxPrice": 1000
		}

		super_admin.api.movies_api.get_movies(query, 400)

	def test_create_empty_movie(self, super_admin):
		body = {}

		super_admin.api.movies_api.create_movie(body, 400)

	def test_get_film(self, super_admin):
		# получаю рандомный фильм
		film = super_admin.api.movies_api.get_movies().json()["movies"][0]
		film_id = film["id"]

		# получаю его же по айдишнику
		response = super_admin.api.movies_api.get_movie(film_id)

		assert response.json()["name"] == film["name"], "Имена не совпадают"

	def test_get_invalid_film(self, super_admin):
		invalid_id = "228481337"

		super_admin.api.movies_api.get_movie(invalid_id, 404)

	def test_film_patch(self, super_admin):
		# получаю рандомный фильм
		film = super_admin.api.movies_api.get_movies().json()["movies"][0]
		film_id = film["id"]

		body = {
			"name": f"{DataGenerator.generate_random_name()}",
			"price": 1488
		}

		response = super_admin.api.movies_api.edit_movie(
			film_id,
			body
		)
		assert response.json()["name"] == body["name"] and \
			response.json()["price"] == body["price"], "Данные не обновлены"
