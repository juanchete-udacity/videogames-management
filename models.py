from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy

import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


'''
Studio
'''


class Studio(db.Model):
    __tablename__ = 'Studio'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    location = Column(db.String)
    videogames = db.relationship(
        'Videogame', backref='studio', lazy=True, cascade='delete')

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


'''
Category
'''


class Category(db.Model):
    __tablename__ = 'Category'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    videogames = db.relationship(
        'Videogame', backref='category', lazy=True, cascade='delete')

    def __init__(self, name):
        self.name = name
        
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


'''
Videogame
'''


class Videogame(db.Model):
    __tablename__ = 'Videogame'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    description = Column(db.String)
    studio_id = Column(db.Integer, db.ForeignKey('Studio.id'))
    category_id = Column(db.Integer, db.ForeignKey('Category.id'))

    def __init__(self, name, description, studio_id, category_id):
        self.name = name
        self.description = description,
        self.studio_id = studio_id,
        self.category_id = category_id

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'studio': self.studio.format(),
            'category': self.category.format()
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())
