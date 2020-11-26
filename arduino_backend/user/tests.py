import json
import unittest
from datetime import datetime, timedelta
from time import sleep
from unittest.mock import MagicMock

from blake3 import blake3
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.exc import InvalidRequestError

from arduino_backend.settings import config
from arduino_backend.testwrapper import databaseTest
from arduino_backend.user import schemas
from arduino_backend.user.models import User


def remove_items_from_obj_except(obj, items):
    for i in obj.__dict__:
        is_in_items = False
        variable_name = [k for k, v in locals().items() if v == i][0]
        for j in items:
            if variable_name == i:
                is_in_items = True
        if not is_in_items:
            del i


class Get_users_tests(databaseTest):
    def test_empty_users(self) -> None:
        empty_users = User.get_users(self.database)
        self.assertEqual(empty_users, [])

    def test_single_user(self) -> None:
        single_user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(single_user)
        self.database.commit()
        user_list = User.get_users(self.database)
        remove_items_from_obj_except(single_user, ["username", "id"])
        result = [single_user]
        self.assertEqual(user_list, result)

    def test_multiple_user(self) -> None:
        first_user = User(username="first", password="hash_mock", salt="salt_mock", uuid="uuid_mock1")
        second_user = User(username="secound", password="hash_mock", salt="salt_mock", uuid="uuid_mock2")
        self.database.add(first_user)
        self.database.add(second_user)
        self.database.commit()
        user_list = User.get_users(self.database)
        remove_items_from_obj_except(first_user, ["username", "id"])
        remove_items_from_obj_except(second_user, ["username", "id"])
        result = [first_user, second_user]
        self.assertEqual(user_list, result)


class Get_user_tests(databaseTest):
    def test_nonexistent_user(self):
        nonexistent_user = User.get_user(self.database, "test")
        self.assertIsNone(nonexistent_user)

    def test_existing_user(self):
        existing_user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(existing_user)
        self.database.commit()
        result = User.get_user(self.database, "test")
        remove_items_from_obj_except(existing_user, ["username", "id"])
        self.assertEqual(result, existing_user)


class Get_user_by_uuid_tests(databaseTest):
    def test_nonexistent_user(self):
        nonexistent_user = User.get_user_by_uuid(self.database, "uuid_mock")
        self.assertIsNone(nonexistent_user)

    def test_existing_user(self):
        existing_user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(existing_user)
        self.database.commit()
        result = User.get_user_by_uuid(self.database, "uuid_mock")
        remove_items_from_obj_except(existing_user, ["username", "id"])
        self.assertEqual(result, existing_user)


class Delete_user_tests(databaseTest):
    def test_deletion(self):
        user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(user)
        self.database.commit()
        deleted_user = user.delete(self.database)
        users = self.database.query(User).all()
        self.assertEqual(deleted_user, user)
        self.assertEqual(users, [])

    def raise_invalid_deletion(self, user: User):
        user.delete(self.database)

    def test_notregistered_deletion(self):
        user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.assertRaises(InvalidRequestError, self.raise_invalid_deletion, user)


class Create_user_tests(databaseTest):
    def test_creation_behaviour(self):
        user_schema = schemas.User(username="test", password="test")
        user = User.create_user(self.database, user_schema)
        users = User.get_users(self.database)
        self.assertEqual([user], users)

    def exception_runner(self, user_schema: schemas.User):
        User.create_user(self.database, user_schema)

    def test_empty_content_error(self):
        empty_schema = schemas.User()
        self.assertRaises(HTTPException, self.exception_runner, empty_schema)

    def test_same_username_exception(self):
        username_schema = schemas.User(username="test", password="test")
        self.exception_runner(username_schema)
        self.assertRaises(HTTPException, self.exception_runner, username_schema)


class Hash_password_tests(unittest.TestCase):
    def test_normal_behaviour(self):
        self.assertEqual(User.hash_password("test", "salt"),
                         blake3(str.encode("test") + str.encode("salt") + str.encode(config.PEPPER)).hexdigest())


class update_user_tests(databaseTest):
    def test_simple_update(self):
        user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(user)
        self.database.commit()
        update_schema = schemas.User(username="test2")
        user.update_user(self.database, update_schema)
        user.username = "test2"
        result = self.database.query(User).first()
        self.assertEqual(result, user)

    def test_complicated_update(self):
        user = User(username="test", password="hash_mock", salt="salt_mock", uuid="uuid_mock")
        self.database.add(user)
        self.database.commit()
        update_schema = schemas.User(password="test")
        updated_user = user.update_user(self.database, update_schema)
        user.salt = updated_user.salt
        user.password = User.hash_password("test", user.salt)
        self.assertEqual(updated_user, user)


class verify_hash_tests(unittest.TestCase):
    def test_correct_hash(self):
        hash_value = blake3(str.encode("test") + str.encode("salt") + str.encode(config.PEPPER)).hexdigest()
        self.assertTrue(User.verify_hash("test", hash_value, "salt"))

    def test_wrong_hash(self):
        self.assertFalse(User.verify_hash("test", "werzdrtutdutdutujtutft", "salt"))


class authentificate_user_tests(databaseTest):
    def test_correct_user(self):
        user = schemas.User(username="test", password="test")
        User.create_user(self.database, user)
        self.assertEqual(User.authenticate_user(self.database, "test", "test"),
                         self.database.query(User).filter(User.username == "test").first())

    def test_wrong_password(self):
        user = schemas.User(username="test", password="test")
        User.create_user(self.database, user)
        self.assertFalse(User.authenticate_user(self.database, "test", "test2"))

    def test_wrong_username(self):
        user = schemas.User(username="test", password="test")
        User.create_user(self.database, user)
        self.assertFalse(User.authenticate_user(self.database, "test2", "test"))


class create_acess_token_tests(unittest.TestCase):
    def test_token_creation(self):
        token = User.create_access_token({})
        self.assertEqual(token, jwt.encode({"exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                                           algorithm=config.ALGORITHM))

    def test_data_dict(self):
        token = User.create_access_token({"foo": "bar"})
        self.assertEqual(token,
                         jwt.encode({"foo": "bar", "exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                                    algorithm=config.ALGORITHM))

    def test_custom_timedelta(self):
        token = User.create_access_token({}, expires_delta=timedelta(minutes=30))
        self.assertEqual(token, jwt.encode({"exp": datetime.utcnow() + timedelta(minutes=30)}, config.JWT_KEY,
                                           algorithm=config.ALGORITHM))


class decode_token_tests(unittest.TestCase):
    def test_correct_decoding(self):
        token = jwt.encode({"user": "foo", "exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        self.assertEqual(User.decode_token(token), "foo")

    def test_wrong_decoding(self):
        token = jwt.encode({"userfalse": "foo", "exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        self.assertFalse(User.decode_token(token))

    def test_manipulated_token(self):
        token = jwt.encode({"user": "foo", "exp": datetime.utcnow() + timedelta(minutes=15)},
                           "b7c18b06a0416d6af22bfaf49abaf7b75956056963e3116e3bbff3be72ed20fe",
                           algorithm=config.ALGORITHM)
        self.assertFalse(User.decode_token(token))

    def test_expired_token(self):
        token = jwt.encode({"user": "foo", "exp": datetime.utcnow() + timedelta(microseconds=1)}, config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        sleep(1)
        self.assertFalse(User.decode_token(token))


class get_current_user_tests(databaseTest):
    def test_normal_behaviour(self):
        user = User.create_user(self.database, schemas.User(username="test", password="test"))
        full_user = self.database.query(User).filter(User.username == user.username).first()
        token = jwt.encode({"user": full_user.uuid, "exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        oauth2_scheme_mock = MagicMock(return_value=token)
        return_user = User.get_current_user(oauth2_scheme_mock(), self.database)
        self.assertEqual(return_user, full_user)

    def current_user_runner(self, oauth_mock: MagicMock):
        User.get_current_user(oauth_mock(), self.database)

    def test_manipulated_token(self):
        user = User.create_user(self.database, schemas.User(username="test", password="test"))
        full_user = self.database.query(User).filter(User.username == user.username).first()
        token = jwt.encode({"userlol": full_user.uuid, "exp": datetime.utcnow() + timedelta(minutes=15)},
                           config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        oauth2_scheme_mock = MagicMock(return_value=token)
        self.assertRaises(HTTPException, self.current_user_runner, oauth2_scheme_mock)

    def test_nonexisting_user(self):
        token = jwt.encode({"user": "lol", "exp": datetime.utcnow() + timedelta(minutes=15)}, config.JWT_KEY,
                           algorithm=config.ALGORITHM)
        oauth2_scheme_mock = MagicMock(return_value=token)
        self.assertEqual(User.get_current_user(oauth2_scheme_mock(), self.database), None)


class user_get_tests(databaseTest):
    def test_statuscode(self):
        response = self.client_mock.get("/user")
        self.assertEqual(response.status_code, 200)

    def test_empty_content(self):
        response = self.client_mock.get("/user")
        self.assertEqual(json.loads(response.content.decode()), [])

    def test_single_content(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.get("/user")
        users = User.get_users(self.database)
        for i in range(len(users)):
            delattr(users[i], "_sa_instance_state")
            users[i] = users[i].__dict__
        self.assertEqual(json.loads(response.content.decode()), users)

    def test_multiple_content(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        User.create_user(self.database, schemas.User(username="lorem2", password="ipsum"))
        response = self.client_mock.get("/user")
        users = User.get_users(self.database)
        for i in range(len(users)):
            delattr(users[i], "_sa_instance_state")
            users[i] = users[i].__dict__
        self.assertEqual(json.loads(response.content.decode()), users)


class single_user_get_tests(databaseTest):
    def test_nonexisting_user(self):
        response = self.client_mock.get("/user/lol")
        self.assertEqual(response.status_code, 404)

    def test_nonexisting_user_content(self):
        response = self.client_mock.get("/user/lol")
        self.assertEqual(json.loads(response.content.decode()), {"detail": "User not found"})

    def test_existing_user_code(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.get("/user/lorem")
        self.assertEqual(response.status_code, 200)

    def test_existing_user_content(self):
        single_user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.get("/user/lorem")
        delattr(single_user, "_sa_instance_state")
        single_user = single_user.__dict__
        #del single_user["uuid"], single_user["password"], single_user["salt"]
        single_user["controllers"] = []
        self.assertEqual(json.loads(response.content.decode()), single_user)


class user_post_test(databaseTest):
    def test_user_creation_code(self):
        response = self.client_mock.post("/user/", json={"username": "lorem", "password": "ipsum"})
        self.assertEqual(response.status_code, 200)

    def test_user_creation_content(self):
        response = self.client_mock.post("/user/", json={"username": "lorem", "password": "ipsum"})
        user = self.database.query(User).filter(User.username == "lorem").first().__dict__
        del user["_sa_instance_state"]
        self.assertEqual(json.loads(response.content.decode()), user)

    def test_json_error(self):
        response = self.client_mock.post("/user/", json={"userlool": "lorem", "password": "ipsum"})
        self.assertEqual(response.status_code, 400)


class user_delete_tests(databaseTest):
    def test_user_deletion(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.delete("/user/lorem", headers={"Authorization": "Bearer " + token})
        self.assertEqual(response.status_code, 200)

    def test_user_deletion_content(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        user = User.get_user(self.database, "lorem")
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.delete("/user/lorem", headers={"Authorization": "Bearer " + token})
        user.controllers = []
        delattr(user, "_sa_instance_state")
        self.assertEqual(response.json(), user.__dict__)

    def test_deletion_without_token(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.delete("/user/lorem")
        self.assertEqual(response.status_code, 401)

    def test_nonexisting_deletion(self):
        User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        user = User.get_user(self.database, "lorem")
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.delete("/user/lol", headers={"Authorization": "Bearer " + token})
        self.assertEqual(response.status_code, 404)

    def test_unallowed_deletion(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        User.create_user(self.database, schemas.User(username="foo", password="bar"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.delete("/user/foo", headers={"Authorization": "Bearer " + token})
        self.assertEqual(response.status_code, 403)


class user_update_tests(databaseTest):
    def test_user_modify(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.put("/user/lorem", headers={"Authorization": "Bearer " + token},
                                        json={"username": "lol", "password": "lol"})
        self.assertEqual(response.status_code, 200)
        self.database.refresh(user)
        updated_user = User.get_user(self.database, "lol")
        delattr(updated_user, "_sa_instance_state")
        # del updated_user["_sa_instance_state"]
        self.assertEqual(response.json(), updated_user.__dict__)

    def test_partial_user_modify(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.put("/user/lorem", headers={"Authorization": "Bearer " + token},
                                        json={"password": "lol"})
        self.database.refresh(user)
        updated_user = User.get_user(self.database, "lorem")
        delattr(updated_user, "_sa_instance_state")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), updated_user.__dict__)

    def test_nonexisting_update(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.put("/user/yeet", headers={"Authorization": "Bearer " + token},
                                        json={"password": "lol"})
        self.assertEqual(response.status_code, 404)

    def test_update_without_token(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        response = self.client_mock.put("/user/lorem", json={"password": "lol"})
        self.assertEqual(response.status_code, 401)

    def test_unauth_update(self):
        user = User.create_user(self.database, schemas.User(username="lorem", password="ipsum"))
        user2 = User.create_user(self.database, schemas.User(username="lol", password="lol"))
        token = User.create_access_token({"user": user.uuid})
        response = self.client_mock.put("/user/lol", headers={"Authorization": "Bearer " + token},
                                        json={"password": "lol"})
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
