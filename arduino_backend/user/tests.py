import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


class databaseTest(unittest.TestCase):
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    database = Session()

    def setUp(self) -> None:
        User.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        User.metadata.drop_all(self.engine)


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


if __name__ == '__main__':
    unittest.main()
