import psycopg2
from resourses.db_creds import DBCreds
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_NAME = DBCreds.MOVIES_NAME
USERNAME = DBCreds.USERNAME
PASSWORD = DBCreds.PASSWORD
HOST = DBCreds.DB_MOVIES_HOST
PORT = DBCreds.MOVIES_PORT

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session() -> Session:
	return SessionLocal()

def connection_to_movies():
	connection = None
	cursor = None

	try:
		connection = psycopg2.connect(
			dbname=DATABASE_NAME,
			user=USERNAME,
			password=PASSWORD,
			host=HOST,
			port=PORT
		)
		print("Connected to database")

		cursor = connection.cursor()

		print("PostgreSQL server information")
		print(connection.get_dsn_parameters(), "\n")

	except Exception as e:
		print("Error while connecting to PostgreSQL", e)

	finally:
		if cursor:
			cursor.close()
		if connection:
			connection.close()
			print("Connection closed")

if __name__ == '__main__':
	connection_to_movies()
