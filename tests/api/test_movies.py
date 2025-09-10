from utils.data_generator import DataGenerator
import pytest


class TestMoviesApi:

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

	@pytest.mark.parametrize(
		"minprice,maxprice,locations,genre_id,expexted_status",
		[
			(200, 800, "SPB", 3, 200),
			(500, 1500, ("SPB", "MKS"), 4, 200),
			(1500, 100, "SPB", 1, 400)
		],
		ids=["Regular query", "Two cities in query", "Bad request (min>max)"]
	)
	def test_param_get_films(self, super_admin, minprice, maxprice, locations, genre_id, expexted_status):
		"""
		Параметризированный тест разных query на movies
		"""
		params = {
			"minPrice": minprice,
			"maxPrice": maxprice,
			"locations": locations,
			"genreId": genre_id
		}
		super_admin.api.movies_api.get_movies(params, expected_status=expexted_status)
