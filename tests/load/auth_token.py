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
        with self.client.post(url="/login", data = {
            "email": SuperAdminCreds.USERNAME,
            "fullName": SuperAdminCreds.PASSWORD
        }) as response:
            self.token = response.json()["accessToken"]

    @task
    def user_list(self):
        self.client.get("/user", headers={"Authorization": f"Bearer {self.token}"})

