#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from re import I
import dateutil.parser
# To use select associated table
from sqlalchemy.sql import select, func
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
moment = Moment(app)



# --------------------
# IMPORT MODELS HERE | 
# TO AVOID CIRCULER  |
# IMPORT             |
# -------------------
from models import *
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  data = []
  view_states = []

  for venue in venues:
      state = venue.state
      all_states = Venue.query.filter_by(state = state).all()

      if state in view_states:
        continue

      item_obj = {
         "city": venue.city,
         "state": venue.state,
         "venues":[]
      }

      # Update visited state array
      view_states.append(state)

      # Loop to group state
      for state in all_states:
          stmt =select([show]).where( show.c.venue_id ==  venue.id)
          result = list(db.session.execute(stmt))
          
          item_obj["venues"].append({
            "id": state.id,
            "name": state.name,
            "num_upcoming_shows": len(result),
          })

      # Save the collection and grouping of states
      data.append(item_obj)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get("search_term", "")

  response = {}
  venues = list(Venue.query.filter(
    Venue.state.ilike(f"%{search_term}%") |
    Venue.name.ilike(f"%{search_term}%")  |
    Venue.city.ilike(f"%{search_term}%") 
    ).all())

  response['count'] = len(venues)
  response["data"] = []
 
  
 
  for venue in venues:

      stmt =select([show]).where( show.c.venue_id ==  venue.id)
      result = list(db.session.execute(stmt))
      
      venue_unit = {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(result),
      }
      response["data"].append(venue_unit)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = []
  past_show = []
  upcoming_show =[]
 

 
  

  stmt =select([show]).where( show.c.venue_id ==  venue.id)
  result = list(db.session.execute(stmt))

  # Past Show & Upcoming show
  for show_details in result:
      print(show_details[0])
      artist = Artist.query.get(show_details[0])

      
      if  show_details[2] < datetime.now():
          past_show.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time":show_details[2].strftime("%m/%d/%Y, %H:%M:%S")
              })
      else:
          upcoming_show.append({
          "artist_id": artist.id,
          "artist_name": artist.name,
          "artist_image_link": artist.image_link,
          "start_time":show_details[2].strftime("%m/%d/%Y, %H:%M:%S")
            })
      
      
  item_obj = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.split(),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_show,
    "upcoming_shows": upcoming_show,
    "past_shows_count": len(past_show),
    "upcoming_shows_count": len(upcoming_show),
  }
     
  data.append( item_obj)

  data = list(filter(lambda d: d['id'] == venue_id, data))[0]
  return render_template('pages/show_venue.html', venue=data)



#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm(request.form)
 
  try:
    new_venue = Venue(
      name =  form.name.data,
      city = form.city.data,
      state = form.state.data,
      address =  form.address.data,
      phone =  form.phone.data,
      genres =   " ".join(form.genres.data),
      facebook_link =  form.facebook_link.data,
      image_link =  form.image_link.data,
      seeking_talent =  form.seeking_talent.data,
      seeking_description =  form.seeking_description.data,
      website_link =  form.website_link.data
    )
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
        print(sys.exc_info())
        flash('Venue ' + request.form['name'] + ' Failure!! to create venue')
        db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')

   # return render_template('pages/home.html')
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #### Gave->  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
      flash('SuccessFully!!! deleted')
    except:
      db.session.rollback()
      flash('Failed to deleted')
    finally:
      db.session.close()
      return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
      item_obj ={
        "id": artist.id,
        "name": artist.name,
      }
      data.append(item_obj)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get("search_term", "")

  response = {}
  artists = list(Artist.query.filter(
    Artist.state.ilike(f"%{search_term}%") |
    Artist.name.ilike(f"%{search_term}%")  |
    Artist.city.ilike(f"%{search_term}%") 
    ).all())

  response['count'] = len(artists)
  response["data"] = []
 
  
 
  for artist in artists:

      stmt =select([show]).where( show.c.artist_id ==  artist.id)
      result = list(db.session.execute(stmt))
      
      venue_unit = {
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": len(result),
      }
      response["data"].append(venue_unit)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  data = []
  upcoming_shows = []
  past_shows = []

  # for artist in artists:
  stmt =select([show]).where( show.c.artist_id ==  artist.id)
  result = list(db.session.execute(stmt))

  # Past Show & Upcoming show
  for show_details in result:
      
      venue_item = Venue.query.get(show_details[1])
     
      if  show_details[2] < datetime.now():
          past_shows.append({
            "venue_id": venue_item.id,
            "e_item_name": venue_item.name,
            "venue_image_link": venue_item.image_link,
            "start_time":show_details[2].strftime("%m/%d/%Y, %H:%M:%S")
              })
      else:
          upcoming_shows.append({
          "venue_id": venue_item.id,
          "venue_name": venue_item.name,
          "venue_image_link": venue_item.image_link,
          "start_time":show_details[2].strftime("%m/%d/%Y, %H:%M:%S")
            })

  item_obj = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  data.append( item_obj)
  
  data = list(filter(lambda d: d['id'] == artist_id, data ))[0]
  return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist_details = Artist.query.get(artist_id)
  artist={
    "id":  artist_details.id,
    "name":  artist_details.name,
    "genres":  artist_details.genres.split(),
    "city":  artist_details.city,
    "state":  artist_details.state,
    "phone":  artist_details.phone,
    "website":  artist_details.website_link,
    "facebook_link":  artist_details.facebook_link,
    "seeking_venue":  artist_details.seeking_venue,
    "seeking_description":  artist_details.seeking_description,
    "image_link":  artist_details.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  try:
      artist_details = Artist.query.get(artist_id)
      artist_details.name =  form.name.data,
      artist_details.genres =  " ".join(form.genres.data),
      artist_details.city =  form.city.data
      artist_details.state =  form.state.data
      artist_details.phone =  form.phone.data
      artist_details.website =  form.website_link.data
      artist_details.facebook_link =  form.facebook_link.data
      artist_details.seeking_description =  form.seeking_description.data
      artist_details.image_link =  form.image_link.data
      artist_details.seeking_venue =  form.seeking_venue.data
     
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      print(sys.exc_info())
      flash('Artist ' + request.form['name'] + ' Failure!!! to  update')
      db.session.rollback()
  finally:
      db.session.close()
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_details = Venue.query.get(venue_id)
  venue={
    
    "name": venue_details.name,
    "genres": venue_details.genres.split(),
    "address":venue_details.address,
    "city":venue_details.city,
    "state": venue_details.state,
    "phone": venue_details.phone,
    "website_link": venue_details.website_link,
    "facebook_link": venue_details.facebook_link,
    "seeking_talent": venue_details.seeking_talent,
    "seeking_description": venue_details.seeking_description,
    "image_link": venue_details.image_link
  }
  print(venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    try:
        venue_details = Venue.query.get(venue_id)

        venue_details.name =  form.name.data,
        venue_details.genres =  " ".join(form.genres.data),
        venue_details.state =  form.state.data
        venue_details.address = form.address.data
        venue_details.city =  form.city.data
        venue_details.phone =  form.phone.data
        venue_details.website_link =  form.website_link.data
        venue_details.facebook_link =  form.facebook_link.data
        venue_details.seeking_description =  form.seeking_description.data
        venue_details.image_link =  form.image_link.data
        venue_details.seeking_talent =  form.seeking_talent.data
      
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        print(sys.exc_info())
        flash('Venue ' + request.form['name'] + ' Failure!!! to  update')
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form =  ArtistForm(request.form)
 
  try:
    new_artist = Artist(
      name =  form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone =  form.phone.data,
      genres =   " ".join(form.genres.data),
      facebook_link =  form.facebook_link.data,
      image_link =  form.image_link.data,
      seeking_venue =  form.seeking_venue.data,
      seeking_description =  form.seeking_description.data,
      website_link =  form.website_link.data
    )
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
        print(sys.exc_info())
        flash('Artist ' + request.form['name'] + ' Failure!! to create Artist')
        db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  s = select([show])
  result = db.session.execute(s)
  for item in result:
      artist = Artist.query.get(item[0])
      venue = Venue.query.get(item[1])
      item_obj ={
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": item[2].strftime("%m/%d/%Y, %H:%M:%S")
      }

      data.append(item_obj)
    
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  print(form.artist_id.data)
  try:
      new_show = show.insert().values(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data ,
        start_time = form.start_time.data
         )
      db.session.execute(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      print(sys.exc_info())
      flash('Failure!! to list Show')
      db.session.rollback()
  finally:
      db.session.close()
      return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# ->  TO lunch use FLASK_APP=app.py FLASK_DEBUG=true flask run
# ->


# Default port:
# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0')

# Or specify port manually:

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

