import os
from flask import Flask, request, abort, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json


from auth import AuthError, requires_auth, AUTH0_DOMAIN, API_AUDIENCE, REDIRECT_URI, CLIENT_ID
from models import db, setup_db, Videogame, Studio, Category

VIDEOGAMES_PER_PAGE = int(os.environ['VIDEOGAMES_PER_PAGE'])


def paginate_videogames(selection, request):
    '''  
    If  there is a page parameter in the request
    we return an slice of the array 
    '''
    if VIDEOGAMES_PER_PAGE is None:
        current_videogames = [videogame.format() for videogame in selection]

    page = request.args.get('page', type=int)

    if page is None:
        current_videogames = [videogame.format() for videogame in selection]
    else:
        start = (page - 1) * VIDEOGAMES_PER_PAGE
        end = start + VIDEOGAMES_PER_PAGE
        videogames = [videogame.format() for videogame in selection]
        current_videogames = videogames[start:end]

    return current_videogames


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    '''
    CORS setup
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    VideoGames API
    '''
    @app.route('/videogames', methods=['GET'])
    def get_videogames():

        selection = Videogame.query.order_by(Videogame.id).all()
        videogames = paginate_videogames(selection, request)

        if len(videogames) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'videogames': videogames,
            'total_videogames': len(videogames),
            'page': request.args.get('page') or False
        })

    @app.route('/videogames', methods=['POST'])
    @requires_auth('post:videogames')
    def create_videogame(payload):
        body = request.get_json()
        name = body.get('name', None)
        description = body.get('description', None)
        studio_id = body.get('studio_id', None)
        category_id = body.get('category_id', None)

        videogame = Videogame(
            name=name,
            description=description,
            studio_id=studio_id,
            category_id=category_id
        )
        videogame.insert()

        return jsonify({
            'success': True,
            'code': 200,
            'created': videogame.format()
        })

    @app.route('/videogames/<int:videogame_id>', methods=['GET'])
    @requires_auth('get:videogames')
    def get_videogame(payload, videogame_id):

        videogame = Videogame.query.filter(
            Videogame.id == videogame_id).one_or_none()

        if videogame is None:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'videogame': videogame.format()
        })

    @app.route('/videogames/<int:videogame_id>', methods=['DELETE'])
    @requires_auth('delete:videogames')
    def delete_videogame(payload, videogame_id):

        videogame = Videogame.query.filter(
            Videogame.id == videogame_id).one_or_none()

        if videogame is None:
            abort(404)

        videogame.delete()
        # TODO exception

        return jsonify({
            'success': True,
            'code': 200,
            'deleted': videogame_id
        })

    @app.route('/videogames/<int:videogame_id>', methods=['PATCH'])
    @requires_auth('patch:videogames')
    def update_videogame(payload, videogame_id):

        videogame = Videogame.query.filter(
            Videogame.id == videogame_id).one_or_none()

        if videogame is None:
            abort(404)

        body = request.get_json()

        name = body.get('name', None)
        description = body.get('description', None)
        studio_id = body.get('studio_id', None)
        category_id = body.get('category_id', None)

        videogame.name = name or videogame.name
        videogame.description = description or videogame.description
        videogame.studio_id = studio_id or videogame.studio_id
        videogame.category_id = category_id or videogame.category_id

        videogame.update()

        return jsonify({
            'success': True,
            'code': 200,
            'updated': videogame.format()
        })

    '''
    Categories
    '''
    @app.route('/categories', methods=['GET'])
    @requires_auth('get:categories')
    def get_categories(payload):

        selection = Category.query.all()
        categories = [category.format() for category in selection]

        return jsonify({
            'success': True,
            'code': 200,
            'categories': categories,
            'total_categories': len(categories)
        })

    @app.route('/categories', methods=['POST'])
    @requires_auth('post:categories')
    def create_category(payload):

        body = request.get_json()
        name = body.get('name', None)

        category = Category(
            name=name
        )
        category.insert()

        return jsonify({
            'success': True,
            'code': 200,
            'created': category.format()
        })

    @app.route('/categories/<int:category_id>', methods=['GET'])
    @requires_auth('get:categories')
    def get_category(payload, category_id):

        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'category': category.format()
        })

    @app.route('/categories/<int:category_id>/videogames', methods=['GET'])
    @requires_auth('get:videogames')
    def get_videogames_from_category(payload, category_id):

        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        videogames = paginate_videogames(category.videogames, request)

        if len(videogames) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'category': category.format(),
            'videogames': videogames,
            'total_videogames': len(category.videogames)
        })

    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    @requires_auth('delete:categories')
    def delete_category(payload, category_id):

        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        category.delete()
        # TODO exception

        return jsonify({
            'success': True,
            'code': 200,
            'deleted': category_id
        })

    @app.route('/categories/<int:category_id>', methods=['PATCH'])
    @requires_auth('patch:categories')
    def update_category(payload, category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)

        category.name = name or category.name

        category.update()

        return jsonify({
            'success': True,
            'code': 200,
            'updated': category.format()
        })

    '''
    Studio API
    '''
    @app.route('/studios', methods=['GET'])
    @requires_auth('get:studios')
    def get_studios(payload):

        selection = Studio.query.all()
        studios = [studio.format() for studio in selection]

        return jsonify({
            'success': True,
            'code': 200,
            'studios': studios,
            'total_studios': len(studios)
        })

    @app.route('/studios', methods=['POST'])
    @requires_auth('post:studios')
    def create_studio(payload):

        body = request.get_json()
        name = body.get('name', None)
        location = body.get('location', None)

        studio = Studio(
            name=name,
            location=location
        )
        studio.insert()

        return jsonify({
            'success': True,
            'code': 200,
            'created': studio.format()
        })

    @app.route('/studios/<int:studio_id>', methods=['GET'])
    @requires_auth('get:studios')
    def get_studio(payload, studio_id):

        studio = Studio.query.filter(Studio.id == studio_id).one_or_none()

        if studio is None:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'studio': studio.format()
        })

    @app.route('/studios/<int:studio_id>/videogames', methods=['GET'])
    @requires_auth('get:videogames')
    def get_videogames_from_studio(payload, studio_id):

        studio = Studio.query.filter(Studio.id == studio_id).one_or_none()

        if studio is None:
            abort(404)

        videogames = paginate_videogames(studio.videogames, request)

        if len(videogames) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'studio': studio.format(),
            'videogames': videogames,
            'total_videogames': len(studio.videogames)
        })

    @app.route('/studios/<int:studio_id>', methods=['DELETE'])
    @requires_auth('delete:studios')
    def delete_studio(payload, studio_id):

        studio = Studio.query.filter(Studio.id == studio_id).one_or_none()

        if studio is None:
            abort(404)

        studio.delete()
        # TODO exception

        return jsonify({
            'success': True,
            'code': 200,
            'deleted': studio_id
        })

    @app.route('/studios/<int:studio_id>', methods=['PATCH'])
    @requires_auth('patch:studios')
    def update_studio(payload, studio_id):
        studio = Studio.query.filter(Studio.id == studio_id).one_or_none()

        if studio is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        location = body.get('location', None)
        studio.name = name or studio.name
        studio.location = location or studio.location

        studio.update()

        return jsonify({
            'success': True,
            'code': 200,
            'updated': studio.format()
        })

    '''
    Healthy check route
    '''

    @app.route('/')
    def healthy():

        return "Healthy!!"

    @app.route('/login')
    def login():
        login_url = f"https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id=VpsuaVE5l6k5XnV0E2fd75aZHzVv676V&redirect_uri={REDIRECT_URI}"
        return render_template('login.html', login_url=login_url)

    @app.route('/login-results')
    def login_results():
        return render_template('login-results.html')

    @app.route('/logout')
    def logout():
        #  user to logout endpoint
        return redirect(f'https://{AUTH0_DOMAIN}/v2/logout?'+
                        f'client_id={CLIENT_ID}&'+
                        'returnTo='+REDIRECT_URI.replace('login-results','login'))

    '''
    Exceptions
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Requires auth"
        }), 401

    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden. Not enough permissions"
        }), 403

    @app.errorhandler(AuthError)
    def authorizationerror(error):

        return jsonify({
            "success": False,
            "error": error.args[1],
            "message": error.args[0]
        }), error.args[1]

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
