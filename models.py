
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
#IMPORTING  APP.py
# from app import app


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#connecting to the local postgresql database definedd in the config file
# app.config.from_object('config')
db = SQLAlchemy()


# TODO: connect to a local postgresql database
        # IN Config file
    
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

show = db.Table('Show',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key = True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key = True),
    db.Column('start_time',db.DateTime, nullable = False )
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String())
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable = False, default= False)
    seeking_description = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
            return f'<Venue ID: {self.id}, Name: {self.name}> , State: {self.state}'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable = False, default= False)
    seeking_description = db.Column(db.String())
    venues = db.relationship('Venue', secondary = show, backref = db.backref('artists', lazy = True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
            return f'<Artist ID: {self.id}, Name: {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

