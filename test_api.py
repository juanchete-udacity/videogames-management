import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Videogame, Studio, Category, setup_db

class VideogamesTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path_test = os.environ['DATABASE_URL']+'_test'
        self.app = create_app()
        self.client = self.app.test_client
        self.db = setup_db(self.app, self.database_path_test)



    def tearDown(self):
            """Executed after reach test"""
            pass
    def test_is_healthy(self):
        res = self.client().get('/')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b"Healthy!!")

    def test_get_videogames(self):
        res = self.client().get('/videogames')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_videogames'])
        self.assertTrue(len(data['videogames']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()