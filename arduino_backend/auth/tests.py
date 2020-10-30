import unittest
from arduino_backend.testwrapper import databaseTest
from arduino_backend.user.models import User
from arduino_backend.user import schemas
from arduino_backend.settings import config
from datetime import timedelta


class authTests(databaseTest):
    def test_no_content(self):
        response = self.client_mock.post("/auth/")
        self.assertEqual(response.status_code, 422)

    def test_wrong_json(self):
        response = self.client_mock.post("/auth/", json={"userlool": "lorem", "password": "ipsum"})
        self.assertEqual(response.status_code, 422)

    def test_correct_code(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.post("/auth/", data="username=lorem&password=ipsum", headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 200)

    def test_correct_content(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.post("/auth/", data="username=lorem&password=ipsum", headers={"Content-Type": "application/x-www-form-urlencoded"})
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = User.create_access_token(
            data={"user": user.uuid}, expires_delta=access_token_expires
        )
        self.assertEqual(response.json(), {"access_token": access_token, "token_type": "bearer"})

    def test_wrong_creds(self):
        response = self.client_mock.post("/auth/", data="username=lorem&password=ipsum", headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 401)


# def test_correct_content(self):


if __name__ == '__main__':
    unittest.main()
