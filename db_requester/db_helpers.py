from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Create and return a test user in the database."""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def create_test_movie(self, movie_data: dict) -> MovieDBModel:
        """Create and return a test movie in the database."""
        movie = MovieDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_user_by_id(self, user_id: str) -> UserDBModel | None:
        """Retrieve a user by ID."""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> UserDBModel | None:
        """Retrieve a user by email."""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def get_movie_by_name(self, name: str) -> MovieDBModel | None:
        """Retrieve a movie by name."""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def get_movie_by_id(self, movie_id: int) -> MovieDBModel | None:
        """Retrieve a movie by ID."""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_any_movie(self) -> MovieDBModel | None:
        """Retrieve any movie from the database."""
        return self.db_session.query(MovieDBModel).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email."""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel) -> None:
        """Delete a user from the database."""
        self.db_session.delete(user)
        self.db_session.commit()

    def delete_user_by_id(self, user_id: int) -> None:
        """Delete a user from the database."""
        self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).delete()

    def delete_movie_by_id(self, movie_id: int) -> None:
        """Delete a movie from the database by ID."""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            self.db_session.delete(movie)
            self.db_session.commit()

    def delete_movie_by_name(self, name: str) -> None:
        """Delete a movie from the database by name."""
        movie = self.get_movie_by_name(name)
        if movie:
            self.db_session.delete(movie)
            self.db_session.commit()

    def cleanup_test_data(self, objects: list) -> None:
        """Delete a list of objects from the database."""
        for obj in objects:
            self.db_session.delete(obj)
        self.db_session.commit()