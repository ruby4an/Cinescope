import requests
from locust import task, HttpUser, between
from resourses.user_creds import SuperAdminCreds


class QuickstartUser(HttpUser):
    """
    Класс для нагрузочного тестирования - пока в базовом формате для теста
    """
    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.token = ''

    wait_time = between(1, 2)

    def on_start(self):
        """
        Новый юзер логинится под кредами супер-админа и записывает токен в атрибут self.token
        """
        response = self.client.post(
            "/login",
            json={
                "email": SuperAdminCreds.USERNAME,
                "password": SuperAdminCreds.PASSWORD
            }
        )
        if response.status_code == 200:
            self.token = response.json()["accessToken"]
        else:
            print(f"Login failed: {response.status_code}, {response.text}")

    @task
    def user_list(self):
        """
        Получаем список юзеров с кредами супер-админа
        """
        self.client.get("/user", headers={"Authorization": "Bearer " + self.token})

