import os
import unittest
import json

from app import create_app
from models import setup_db, Videogame, Category, Studio


class VideogamesTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path_test = os.environ['DATABASE_URL']+'_test'
        self.app = create_app(test_mode=True)
        self.client = self.app.test_client
        self.db = setup_db(self.app, self.database_path_test)
        # JWT tokens for each role for unit testing
        self.TOKEN_ROLE_USER = os.environ['TOKEN_ROLE_USER']
        self.TOKEN_ROLE_STUDIO = os.environ['TOKEN_ROLE_STUDIO']
        self.TOKEN_ROLE_MANAGER = os.environ['TOKEN_ROLE_MANAGER']
        # JSON Bodies for each endpoint
        self.new_videogame = {
            'name': 'Test Videogame Name',
            'description': 'Test Videogame Description',
            'studio_id': 1,
            'category_id': 1
        }
        self.new_studio = {
            'name': 'Test Studio Name',
            'Location': 'Test Studio Location'
        }
        self.new_category = {
            'name': 'Test Category Name'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Is Running?
    def test_is_healthy(self):
        res = self.client().get('/')
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, b"Healthy!!")
    
    '''
    POST TESTS
    '''

    # POST /studios with Auth Manager
    def test_post_studios_auth(self):
        res = self.client().post(
            '/studios', json=self.new_studio,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # POST /studios with Auth but not enough
    def test_post_studios_auth_user(self):
        res = self.client().post(
            '/studios', json=self.new_studio,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # POST /studios without Auth
    def test_post_studios_unauth(self):
        res = self.client().post(
            '/studios', json=self.new_studio
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # POST /categories with Auth Manager 200
    def test_post_categories_auth(self):
        res = self.client().post(
            '/categories', json=self.new_category,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # POST /categories with Auth but not enough
    def test_post_categories_auth_user(self):
        res = self.client().post(
            '/categories', json=self.new_category,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # POST /categories without Auth
    def test_post_categories_unauth(self):
        res = self.client().post(
            '/categories', json=self.new_category
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # POST /videogames with Auth Manager
    def test_post_videogames_auth(self):
        res = self.client().post(
            '/videogames', json=self.new_videogame,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # POST /videogames with Auth but not enough
    def test_post_videogames_auth_user(self):
        res = self.client().post(
            '/videogames', json=self.new_videogame,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # POST /videogames without Auth
    def test_post_videogames_unauth(self):
        res = self.client().post(
            '/videogames', json=self.new_videogame
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    PATCH Tests
    '''

    # PATCH /videogames with Auth Manager
    def test_patch_videogames_auth(self):
        res = self.client().patch(
            '/videogames/1', json=self.new_videogame,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # PATCH /videogames with Auth but not enough
    def test_patch_videogames_auth_user(self):
        res = self.client().patch(
            '/videogames/1', json=self.new_videogame,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # PATCH /videogames without Auth
    def test_patch_videogames_unauth(self):
        res = self.client().patch(
            '/videogames/1', json=self.new_videogame
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # PATCH /videogames without non existant videogame
    def test_patch_videogames_not_found(self):
        res = self.client().patch(
            '/videogames/1000000', json=self.new_videogame,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # PATCH /studios with Auth Manager
    def test_patch_studios_auth(self):
        res = self.client().patch(
            '/studios/1', json=self.new_studio,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # PATCH /studios with Auth but not enough
    def test_patch_studios_auth_user(self):
        res = self.client().patch(
            '/studios/1', json=self.new_studio,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # PATCH /studios without Auth
    def test_patch_studios_unauth(self):
        res = self.client().patch(
            '/studios/1', json=self.new_studio
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # PATCH /studios without non existant studio
    def test_patch_studios_not_found(self):
        res = self.client().patch(
            '/studios/1000000', json=self.new_studio,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # PATCH /categories with Auth Manager
    def test_patch_categories_auth(self):
        res = self.client().patch(
            '/categories/1', json=self.new_category,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    # PATCH /categories with Auth but not enough
    def test_patch_categories_auth_user(self):
        res = self.client().patch(
            '/categories/1', json=self.new_category,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # PATCH /categories without Auth
    def test_patch_categories_unauth(self):
        res = self.client().patch(
            '/categories/1', json=self.new_category
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # PATCH /categories without non existant category
    def test_patch_categories_not_found(self):
        res = self.client().patch(
            '/categories/1000000', json=self.new_category,
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    GET Tests
    '''
    # GET /videogames

    def test_get_videogames(self):
        res = self.client().get('/videogames')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_videogames'])
        self.assertTrue(len(data['videogames']))

    # GET /videogames paginated
    def test_get_videogames_unauth_paginated(self):
        res = self.client().get(
            '/videogames?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_videogames'])
        self.assertTrue(len(data['videogames']))

    # GET /videogames paginated more than games
    def test_get_videogames_unauth_not_found_paginated(self):
        res = self.client().get(
            '/videogames?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # GET /videogames/1 without Auth
    def test_get_videogames_detail_unauth(self):
        res = self.client().get('/videogames/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
       

    # GET /videogames/1 with Auth
    def test_get_videogames_detail_auth(self):
        res = self.client().get(
            '/videogames/1',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET /categories non auth
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # GET /categories with auth
    def test_get_categories_auth(self):
        res = self.client().get(
            '/categories',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # GET /categories/1/videogames with Auth
    def test_get_videogames_from_category_auth(self):
        res = self.client().get(
            '/categories/1/videogames',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_STUDIO}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['videogames'])

    # GET /studios non auth
    def test_get_studios(self):
        res = self.client().get('/studios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # GET /studios with auth
    def test_get_studios_auth(self):
        res = self.client().get(
            '/studios',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_studios'])
        self.assertTrue(len(data['studios']))

    # GET /studios/1/videogames with Auth
    def test_get_videogames_from_studio_auth(self):
        res = self.client().get(
            '/studios/1/videogames',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_STUDIO}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['videogames'])

    '''
    DELETE Tests
    '''
    def test_delete_videogames_auth_user(self):
        res = self.client().delete(
            '/videogames/1',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # DELETE /videogames without Auth
    def test_delete_videogames_unauth(self):
        res = self.client().delete(
            '/videogames/1'
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # DELETE /videogames without non existant videogame
    def test_delete_videogames_not_found(self):
        res = self.client().delete(
            '/videogames/1000000',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # DELETE from /videogames with Auth Manager
    def test_delete_videogames_auth(self):
        videogame = Videogame.query.order_by(Videogame.id.desc()).first()
        res = self.client().delete(
            '/videogames/'+str(videogame.id),
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE /categories with Auth but not enough

    def test_delete_categories_auth_user(self):
        res = self.client().delete(
            '/categories/1',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # DELETE /categories without Auth
    def test_delete_categories_unauth(self):
        res = self.client().delete(
            '/categories/1'
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # DELETE /categories without non existant category
    def test_delete_categories_not_found(self):
        res = self.client().delete(
            '/categories/1000000',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # DELETE /categories with Auth Manager
    def test_delete_categories_auth(self):
        category = Category.query.order_by(Category.id.desc()).first()
        res = self.client().delete(
            '/categories/'+str(category.id),
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE /studios with Auth but not enough
    def test_delete_studios_auth_user(self):
        res = self.client().delete(
            '/studios/1',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_USER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # DELETE /studios without Auth
    def test_delete_studios_unauth(self):
        res = self.client().delete(
            '/studios/1'
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # DELETE /studios without non existant studio
    def test_delete_studios_not_found(self):
        res = self.client().delete(
            '/studios/1000000',
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # DELETE /studios with Auth Manager
    def test_delete_studios_auth(self):
        studio = Studio.query.order_by(Studio.id.desc()).first()
        res = self.client().delete(
            '/studios/'+str(studio.id),
            headers={'authorization': f"Bearer {self.TOKEN_ROLE_MANAGER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # DELETE /videogames with Auth but not enough
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
