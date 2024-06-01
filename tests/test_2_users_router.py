from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
user_tokens = {}


class TestSignup:
    def test_usually(self):
        global user_tokens

        login = "test_user1"
        password = "password"

        response = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": False,
            "admin_token": "empty",
        })
        answer = response.json()
        user_tokens["1"] = answer["token"]

        assert response.status_code == 200
        assert answer["id"] == 1
        assert answer["login"] == login
        assert answer["is_admin"] is False

    def test_already_exists(self):
        login = "test_user1"
        password = "password"

        response = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": False,
            "admin_token": "empty",
        })

        assert response.status_code == 404
        assert response.json()['detail'] == f"User with login '{login}' is already exists"

    def test_admin(self):
        global user_tokens

        login = "test_admin1"
        password = "password"
        token = "toster123"

        response = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": True,
            "admin_token": token,
        })
        answer = response.json()
        user_tokens["2"] = answer["token"]

        assert response.status_code == 200
        assert answer["id"] == 2
        assert answer["login"] == login
        assert answer["is_admin"] is True

    def test_wrong_admin_token(self):
        login = "test_admin2"
        password = "password"
        token = "wrong"

        response = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": True,
            "admin_token": token,
        })
        assert response.status_code == 404
        assert response.json()['detail'] == f"Entered wrong admin-token '{token}'"


class TestSignin:
    def test_usually(self):
        global user_tokens

        login = "test_user1"
        password = "password"

        response = client.post("/users/signin", json={
            "login": login,
            "password": password,
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer["id"] == 1
        assert answer["login"] == login
        assert answer["is_admin"] is False
        assert answer["token"] == user_tokens["1"]

    def test_wrong_password(self):
        login = "test_user1"
        password = "wrong"

        response = client.post("/users/signin", json={
            "login": login,
            "password": password,
        })

        assert response.status_code == 404
        assert response.json()["detail"] == f"Entered wrong password for login '{login}'"


class TestRemove:
    def test_usually(self):
        global user_tokens

        login = "test_user_for_removing"
        password = "password"

        response1 = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": False,
            "admin_token": "empty",
        })
        answer = response1.json()
        user_tokens["3"] = answer["token"]

        assert response1.status_code == 200
        assert answer["id"] == 3

        response2 = client.post("/users/remove", json={
            "login": login,
            "password": password,
        })
        answer = response2.json()

        assert response2.status_code == 200
        assert answer is True

    def test_wrong_password(self):
        global user_tokens

        login = "test_user_for_removing"

        response1 = client.post("/users/signup", json={
            "login": login,
            "password": "password1",
            "is_admin": False,
            "admin_token": "empty",
        })
        answer = response1.json()
        user_tokens["4"] = answer["token"]

        assert response1.status_code == 200
        assert answer["id"] == 4

        response2 = client.post("/users/remove", json={
            "login": login,
            "password": "password2",
        })
        answer = response2.json()

        assert response2.status_code == 404
        assert answer["detail"] == f"Entered wrong password for login '{login}'"


class TestChange:
    def test_usually(self):
        global user_tokens

        login = "test_user2"
        password = "password"

        response1 = client.post("/users/signup", json={
            "login": login,
            "password": password,
            "is_admin": False,
            "admin_token": "empty",
        })
        answer = response1.json()
        user_tokens["5"] = answer["token"]

        assert response1.status_code == 200
        assert answer["id"] == 5

        response2 = client.post("/users/change", json={
            "login": login,
            "password": password,
            "new_login": login + "_new",
            "new_password": password + "_new",
        })
        answer = response2.json()

        assert response2.status_code == 200
        assert answer["id"] == 5
        assert answer["login"] == login + "_new"
        assert answer["token"] == user_tokens["5"]
        assert answer["is_admin"] is False

        response3 = client.post("/users/signin", json={
            "login": login + "_new",
            "password": password + "_new",
        })
        answer = response3.json()

        assert response3.status_code == 200
        assert answer["id"] == 5

    def test_wrong_password(self):
        global user_tokens

        login = "test_user2_new"
        password = "wrong"

        response = client.post("/users/change", json={
            "login": login,
            "password": password,
            "new_login": "something",
            "new_password": "something",
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"Entered wrong password for login '{login}'"


class TestGet:
    def test_by_id(self):
        user_id = 1

        response = client.get("/users/get", params={
            "id": user_id
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer["login"] == "test_user1"

    def test_by_wrong_id(self):
        user_id = 0

        response = client.get("/users/get", params={
            "id": user_id
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"No user with id = '{user_id}'"

    def test_by_login(self):
        user_login = "test_user1"

        response = client.get("/users/get", params={
            "login": user_login
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer["id"] == 1

    def test_by_wrong_login(self):
        user_login = "no_user"

        response = client.get("/users/get", params={
            "login": user_login
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"No user with login = '{user_login}'"

    def test_by_token(self):
        user_token = user_tokens["1"]

        response = client.get("/users/get", params={
            "token": user_token
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer["id"] == 1

    def test_by_wrong_token(self):
        user_token = "bad_token"

        response = client.get("/users/get", params={
            "token": user_token
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"No user with token = '{user_token}'"


class TestIsAdmin:
    def test_by_id(self):
        user_id = 2

        response = client.get("/users/is_admin", params={
            "id": user_id
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer is True

    def test_by_wrong_id(self):
        user_id = 1

        response = client.get("/users/is_admin", params={
            "id": user_id
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"User with id '{user_id}' isn't admin"

    def test_by_login(self):
        user_login = "test_admin1"

        response = client.get("/users/is_admin", params={
            "login": user_login
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer is True

    def test_by_wrong_login(self):
        user_login = "test_user1"

        response = client.get("/users/is_admin", params={
            "login": user_login
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"User with login '{user_login}' isn't admin"

    def test_by_token(self):
        user_token = user_tokens["2"]

        response = client.get("/users/is_admin", params={
            "token": user_token
        })
        answer = response.json()

        assert response.status_code == 200
        assert answer is True

    def test_by_wrong_token(self):
        user_token = user_tokens["1"]

        response = client.get("/users/is_admin", params={
            "token": user_token
        })
        answer = response.json()

        assert response.status_code == 404
        assert answer["detail"] == f"User with token '{user_token}' isn't admin"
