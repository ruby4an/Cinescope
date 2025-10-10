import random
import string
from datetime import datetime as dt
from faker import Faker
from uuid import uuid4

faker = Faker()


class DataGenerator:

	@staticmethod
	def generate_random_email():
		random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
		return f"kek{random_string}@gmail.com"

	@staticmethod
	def generate_random_name():
		return f"{faker.first_name()} {faker.last_name()}"

	@staticmethod
	def generate_random_password():
		"""
		Генерация пароля, соответствующего требованиям:
		- Минимум 1 буква.
		- Минимум 1 цифра.
		- Допустимые символы.
		- Длина от 8 до 20 символов.
		"""
		# Гарантируем наличие хотя бы одной буквы и одной цифры
		letters = random.choice(string.ascii_letters)  # Одна буква
		digits = random.choice(string.digits)  # Одна цифра

		# Дополняем пароль случайными символами из допустимого набора
		special_chars = "?@#$%^&*|:"
		all_chars = string.ascii_letters + string.digits + special_chars
		remaining_length = random.randint(6, 18)  # Остальная длина пароля
		remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

		# Перемешиваем пароль для рандомизации
		password = list(letters + digits + remaining_chars)
		random.shuffle(password)

		return ''.join(password)

	@staticmethod
	def generate_random_int(value: int) -> int:
		return random.randint(1488, value)

	@staticmethod
	def generate_user_data() -> dict:
		return {
			'id': f"{uuid4()}",
			'email': DataGenerator.generate_random_email(),
			'full_name': DataGenerator.generate_random_name(),
			'password': DataGenerator.generate_random_password(),
			'created_at': dt.now(),
			'updated_at': dt.now(),
			'verified': False,
			'banned': False,
			'roles': '{USER}'
		}

	@staticmethod
	def generate_movie_data() -> dict:
		return {
			'name': faker.sentence(nb_words=3).rstrip('.'),
			'price': random.randint(5, 100),
			'description': faker.text(max_nb_chars=200),
			'image_url': faker.image_url(),
			'location': random.choice(['MSK', 'SPB']),
			'published': random.choice([True, False]),
			'rating': round(random.uniform(1.0, 10.0), 1),
			'genre_id': random.randint(1, 10),
			'created_at': dt.now()
		}
