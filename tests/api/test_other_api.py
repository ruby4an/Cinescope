import pytest
from sqlalchemy.orm import Session
import logging as logger
from db_models.account_transaction import AccountTransactionTemplate
from db_models.movie import MovieDBModel
from db_requester.db_helpers import DBHelper
from utils.data_generator import DataGenerator
import allure
import random


def test_movie_create_delete(db_session: Session,
                             db_helper: DBHelper,
                             created_test_movie: MovieDBModel):
    # проверка отсутствия филмьа в базе
    # assert db_helper.get_movie_by_name("Ебнутая комедия игорь подзалупный") is None
    # создание фильма
    movie_id = created_test_movie.id
    assert movie_id is not None, "ID созданного фильма не должен быть None"
    # проверка что фильм создался в базе
    movie_in_db = db_helper.get_movie_by_id(movie_id)
    assert movie_in_db is not None, f"Фильм с ID {movie_id} не найден в базе"
    assert movie_in_db.name == created_test_movie.name, "Имя фильма в базе не совпадает с ожидаемым"
    # удаление фильма и проверка на это происходит в фикстуре created


@allure.epic("Тестирование транзакций в базе")
@allure.feature("Тестирование транзакций между счетами")
@pytest.mark.xfail(strict=True, reason="Тест проверяет откат транзакции при ошибке")
@pytest.mark.skip(reason="Прошла кривая миграция таблицы - тест ее не находит")
class TestAccountTransactionTemplate:
    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "ruby4an")
    @allure.title("Тестирование транзакций между счетами Stan и Bob")
    def test_accounts_transaction_template(self, db_session: Session):
        # =========== Подготовка тестовых данных ===========
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(
                user=f"Stan_{DataGenerator.generate_random_int(100000)}",
                balance=1000
            )
            bob = AccountTransactionTemplate(
                user=f"Bob_{DataGenerator.generate_random_int(100000)}",
                balance=500
            )
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция для перевода денег между счетами")
        @allure.description("""
        функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
        и вызывая метод transfer_money, мы как будто делаем запрос в api_manager.movies_api.transfer_money
        """)
        def transfer_money(session: Session, from_account: str, to_account: str, amount: int):
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            if from_account.balance<amount:
                raise ValueError("Недостаточно средств для перевода")

            from_account.balance -= amount
            to_account.balance += amount

            session.commit()

        # =========== Выполнение теста ===========

        with allure.step("Проверка начальных балансов счетов"):
            assert stan.balance == 1000, f"Начальный баланс Стэна должен быть 1000, но он {stan.balance}"
            assert bob.balance == 500, f"Начальный баланс Боба должен быть 500, но он {bob.balance}"

        try:
            with allure.step("Перевод денег от Stan к Bob (ожидается ошибка из-за недостатка средств)"):

                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=1100)

            with allure.step("Проверка балансов после перевода (этот шаг не должен быть достигнут в этом тесте)"):

                assert stan.balance == 800, f"Баланс Стэна после перевода должен быть 800, но он {stan.balance}"
                assert bob.balance == 700, f"Баланс Боба после перевода должен быть 700, но он {bob.balance}"

        except Exception as e:
            with allure.step("Обработка ошибки и откат транзакции"):
                db_session.rollback()
                # Проверка что балансы остались неизменными
                assert stan.balance == 1000, f"Баланс Стэна должен остаться 1000 после отката, но он {stan.balance}"
                logger.info("Откат транзакции выполнен успешно для Стэна")
                assert bob.balance == 500, f"Баланс Боба должен остаться 500 после отката, но он {bob.balance}"
                logger.info("Откат транзакции выполнен успешно для Боба")
                pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаление тестовых данных из базы данных"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()

def test_delete_movie(super_admin, db_session: Session, db_helper: DBHelper):

    movie_id = 54
    try:
        super_admin.api.movies_api.get_movie(movie_id, expected_status=200)
        logger.info(f"Фильм с ID {movie_id} уже существует в базе.")
    except ValueError:
        # Если фильм не найден, создаем его
        movie_data = DataGenerator.generate_movie_data()
        movie_data['id'] = movie_id

        db_helper.create_test_movie(movie_data)
        assert db_helper.get_movie_by_id(movie_id) is not None, f"Фильм с ID {movie_id} не был создан в базе."

        logger.info(f"Фильм с ID {movie_id} был создан для теста удаления.")

    finally:
        # проверяю связь между API и базой
        assert (super_admin.api.movies_api.get_movie(movie_id).json()['name'] ==
            db_helper.get_movie_by_id(movie_id).name), "Имя фильма не совпадает с ожидаемым"

        # удаляю фильм
        super_admin.api.movies_api.delete_movie(movie_id)
        assert db_helper.get_movie_by_id(movie_id) is None, f"Фильм с ID {movie_id} не был удален из базы."
        logger.info(f"Фильм с ID '{movie_id}' был успешно удален из базы.")

@allure.title("Тест с перезапусками")
@pytest.mark.flaky(reruns=3)
def test_with_retries(delay_between_retries):
    with allure.step("Шаг 1: Проверка случайного значения"):
        result = random.choice([True, False])
        assert result, "Случайное значение оказалось False, тест будет перезапущен"




