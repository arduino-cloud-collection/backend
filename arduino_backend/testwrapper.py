import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import remove
from arduino_backend.user.models import User
from arduino_backend.main import app
from fastapi.testclient import TestClient


class databaseTest(unittest.TestCase):
    client_mock = TestClient(app)

    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=self.engine)
        self.database = self.Session()
        User.metadata.create_all(self.engine)

    def tearDown(self) -> None:
        User.metadata.drop_all(self.engine)
        remove("test.db")
