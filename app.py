import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json


from auth import AuthError, requires_auth
from models import db, setup_db, Videogame, Studio, Category

app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)
CORS(app)

'''
VideoGames API
'''
@app.route('/videogames', methods=['GET'])
def get_videogames():

    selection = Videogame.query.all()
    videogames = [videogame.format() for videogame in selection]

    return jsonify({
        'success': True,
        'code': 200,
        'videogames': videogames,
        'total_videogames': len(videogames)
    })


@app.route('/videogames', methods=['POST'])
def create_videogame():
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
def get_videogame(videogame_id):

    videogame = Videogame.query.filter(Videogame.id==videogame_id).one_or_none()

    if videogame is None:
      abort(404)
    
    return jsonify({
        'success': True,
        'code': 200,
        'videogame': videogame.format()
    })


@app.route('/videogames/<int:videogame_id>', methods=['DELETE'])
def delete_videogame(videogame_id):

    videogame = Videogame.query.filter(Videogame.id==videogame_id).one_or_none()

    if videogame is None:
      abort(404)

    videogame.delete()
    #TODO exception

    return jsonify({
        'success': True,
        'code': 200,
        'deleted': videogame_id
    })
    


@app.route('/videogames/<int:videogame_id>', methods=['PATCH'])
def update_videogame(videogame_id):

    videogame = Videogame.query.filter(Videogame.id==videogame_id).one_or_none()

    if videogame is None:
      abort(404)
    
    body = request.get_json()
    name = body.get('name', None)
    description = body.get('description', None)
    studio_id = body.get('studio_id', None)
    category_id = body.get('category_id', None)

    videogame.name =  name or videogame.name
    videogame.description =  description or videogame.description
    videogame.studio_id =  studio_id or videogame.studio_id
    videogame.category_id =  category_id or videogame.category_id

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
def get_categories():

    selection = Category.query.all()
    categories = [category.format() for category in selection]

    return jsonify({
        'success': True,
        'code': 200,
        'categories': categories,
        'total_categories': len(categories)
    })


@app.route('/categories', methods=['POST'])
def create_category():

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
def get_category(category_id):

    category = Category.query.filter(Category.id==category_id).one_or_none()

    if category is None:
      abort(404)
    
    return jsonify({
        'success': True,
        'code': 200,
        'category': category.format()
    })


@app.route('/categories/<int:category_id>/videogames', methods=['GET'])
def get_videogames_from_category(category_id):
    
    category = Category.query.filter(Category.id==category_id).one_or_none()
    
    if category is None:
      abort(404)
    
    selection = Videogame.query.filter(Videogame.category_id == category_id).all()
    if len(selection) == 0:
      videogames = []
    else:
      videogames = [videogame.format() for videogame in selection]
       
    return jsonify({
        'success': True,
        'code': 200,
        'category': category.format(),
        'videogames': videogames
    })
    


@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):

    category = Category.query.filter(Category.id==category_id).one_or_none()

    if category is None:
      abort(404)

    category.delete()
    #TODO exception

    return jsonify({
        'success': True,
        'code': 200,
        'deleted': category_id
    })


@app.route('/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    category = Category.query.filter(Category.id==category_id).one_or_none()

    if category is None:
      abort(404)
    
    body = request.get_json()
    name = body.get('name', None)
    
    category.name =  name or category.name
    
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
def get_studios():

    selection = Studio.query.all()
    studios = [studio.format() for studio in selection]

    return jsonify({
        'success': True,
        'code': 200,
        'studios': studios,
        'total_studios': len(studios)
    })


@app.route('/studios', methods=['POST'])
def create_studio():

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
def get_studio(studio_id):

    studio = Studio.query.filter(Studio.id==studio_id).one_or_none()

    if studio is None:
      abort(404)
    
    return jsonify({
        'success': True,
        'code': 200,
        'studio': studio.format()
    })


@app.route('/studios/<int:studio_id>/videogames', methods=['GET'])
def get_videogames_from_studio(studio_id):
    
    studio = Studio.query.filter(Studio.id==studio_id).one_or_none()
    
    if studio is None:
      abort(404)
    
    selection = Videogame.query.filter(Videogame.studio_id == studio_id).all()
    if len(selection) == 0:
      videogames = []
    else:
      videogames = [videogame.format() for videogame in selection]
       
    return jsonify({
        'success': True,
        'code': 200,
        'studio': studio.format(),
        'videogames': videogames
    })
    


@app.route('/studios/<int:studio_id>', methods=['DELETE'])
def delete_studio(studio_id):

    studio = Studio.query.filter(Studio.id==studio_id).one_or_none()

    if studio is None:
      abort(404)

    studio.delete()
    #TODO exception

    return jsonify({
        'success': True,
        'code': 200,
        'deleted': studio_id
    })


@app.route('/studios/<int:studio_id>', methods=['PATCH'])
def update_studio(studio_id):
    studio = Studio.query.filter(Studio.id==studio_id).one_or_none()

    if studio is None:
      abort(404)
    
    body = request.get_json()
    name = body.get('name', None)
    location = body.get('location', None)
    studio.name =  name or studio.name
    studio.location =  location or studio.location
    
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
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def authorizationerror(error):

    return jsonify({
        "success": False,
        "error": error.args(1),
        "message": error.args(0)
    }), error.args(1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
