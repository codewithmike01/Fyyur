
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#IMPORTING  APP.py
from app import app


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#connecting to the local postgresql database definedd in the config file
app.config.from_object('config')
db = SQLAlchemy(app)
db.app = app
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mike-savy:dreamlife!@localhost:5432/fyyur'


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
