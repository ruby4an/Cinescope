from custom_requester.custom_requester import CustomRequester
from constants.constants import MOVIES_ENDPOINT


class MoviesAPI(CustomRequester):
    MOVIE_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self._session = session
        super().__init__(session, self.MOVIE_BASE_URL)

    def get_movies(self, params: dict = None, expected_status=200):
        return self.send_request(
            "GET",
            MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status,
            need_logging=False
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=data,
            expected_status=expected_status
        )

    def edit_movie(self, movie_id, data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
