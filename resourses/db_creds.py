import os
from dotenv import load_dotenv

load_dotenv()


class DBCreds:
	USERNAME = os.getenv('DB_USERNAME')
	PASSWORD = os.getenv('DB_PASSWORD')
	MOVIES_NAME = os.getenv('DB_MOVIES_NAME')
	MOVIES_PORT = os.getenv('DB_MOVIES_PORT')
	DB_MOVIES_HOST = os.getenv('DB_MOVIES_HOST')
