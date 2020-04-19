import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from ../app import app
from ../models import Videogame, Studio, Category

class VideogamesTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = os.environ.get("PSQL_USER")
        self.database_password = os.environ.get("PSQL_PWD")
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user, self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

    def tearDown(self):
            """Executed after reach test"""
            pass
    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()