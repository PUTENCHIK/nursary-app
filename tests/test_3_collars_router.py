from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def get_token(login: str, password: str):
    response = client.post("/users/signin", json={
        "login": login,
        "password": password,
    })

    return response.json()


class Test:
    def test_1(self):
        pass
