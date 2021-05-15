#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#



import dateutil.parser
import babel
from flask import  render_template, request, flash, redirect, url_for
import logging
from logging import  Formatter, FileHandler
from forms import *
from models import Artist , Venue , Shows ,app ,db 
from functions import *



def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



#functions in function.py
#models in models.py




@app.route('/', methods=['DELETE','POST','GET'])
def index():
    return render_template('pages/home.html')



@app.route('/venues')
def venues():
  try:
    venues = countvins()

    return render_template('pages/venues.html', areas=venues)
  except:
        return render_template('errors/500.html')

@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    searchterm = request.form.get('search_term', '')

    result = search2(searchterm)

    return render_template('pages/search_venues.html',
                           results=result, search_term=searchterm)
  except:
        return render_template('errors/500.html')


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
  try:
    data = getvenue(venue_id)
    if(data == {}):
        return render_template('errors/404.html')
    else:
        return render_template('pages/show_venue.html', venue=data)
  except:
        return render_template('errors/404.html')

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    try:
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)
    except:
        return render_template('errors/500.html')

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    data = request.form
    form = VenueForm(data, csrf_enabled=False)
    if form.validate():
      try:
          ven = Venue(
              name=data['name'],
              city=data['city'],
              state=data['state'],
              address=data['address'],
              phone=data['phone'],
              image_link=data['image_link'],
              genres=(
                  ','.join(
                      data.getlist('genres'))),
              facebook_link=data['facebook_link'])
          db.session.add(ven)
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
          db.session.close()
          return render_template('pages/home.html')
      except Exception:
          flash(
              'An error occurred. Venue ' +
              data['name'] +
              ' could not be listed.')
          return render_template('errors/500.html')
    else:
      flash(form.errors)
      return redirect(url_for('create_venue_form'))
      


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Shows.query.filter_by(Venue_id=venue_id).delete()
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        print('deleted: ', venue_id)
        return redirect(url_for('index'))
    except:
        return render_template('errors/500.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')          #viewall
def artists():
    try:
        data = Artist.query.all()
        return render_template('pages/artists.html', artists=data)
    except:
        return render_template('/errors/500.html')

@app.route('/artists/search', methods=['POST'])                 
def search_artists():
  try:
    query = request.form.get('search_term', '')
    data = search(query)
    return render_template('pages/search_artists.html',
                           results=data, search_term=query)
  except:
        return render_template('errors/500.html')

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  try:
    data = artistsearch(artist_id)
    return render_template('pages/show_artist.html', artist=data)
  except:
        return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------

#--------------------------------------------
#edit artist

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        form = ArtistForm()
        data = Artist.query.get(artist_id)
        gen = data.genres
        data.genres = gen.split(',')
        # TODO: populate form with fields from artist with ID <artist_id>
        return render_template('forms/edit_artist.html', form=form, artist=data)
    except:
        return render_template('errors/404.html')

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form, csrf_enabled=False)
    if form.validate():
      try:  
        data = request.form
        artist = Artist.query.get(artist_id)
        artist.name = data['name']
        artist.city = data['city']
        artist.state = data['state']
        artist.phone = data['phone']
        artist.genres = ','.join(data.getlist('genres'))
        artist.image_link = data['image_link']
        artist.facebook_link = data['facebook_link']
        db.session.commit()
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))
      except:
        return render_template('errors/500.html')
    else:
      flash(form.errors)
      return redirect('/artists/'+str(artist_id)+'/edit')


#------------------------------------------------
#edit venue
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    try:   
        form = VenueForm()
        data1 = Venue.query.get(venue_id)
        gen = data1.genres
        data1.genres = gen.split(',')
        # TODO: populate form with values from venue with ID <venue_id>
        return render_template('forms/edit_venue.html', form=form, venue=data1)
    except:
        return render_template('errors/404.html') 

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form, csrf_enabled=False)
    if form.validate():
      try:
        data = request.form
        venue = Venue.query.get(venue_id)
        venue.name = data['name']
        venue.city = data['city']
        venue.state = data['state']
        venue.phone = data['phone']
        venue.genres = ','.join(data.getlist('genres'))
        venue.image_link = data['image_link']
        venue.facebook_link = data['facebook_link']
        db.session.commit()
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))
      except:
        return render_template('errors/500.html')
    else:
      flash(form.errors)
      return redirect('/venues/'+str(venue_id)+'/edit')

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    try:
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)
    except:
        return render_template('pages/home.html')

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    data = request.form
    form = ArtistForm(request.form, csrf_enabled=False)
    if form.validate():
        try:
            print(data['city'])
            artist = Artist(
                name=data['name'],
                city=data['city'],
                state=data['state'],
                phone=data['phone'],
                image_link=data['image_link'],
                genres=(
                    ','.join(
                        data.getlist('genres'))),
                facebook_link=data['facebook_link'])
            db.session.add(artist)
            db.session.commit()
            flash('artist ' + request.form['name'] + ' was successfully listed!')
            db.session.close()
            return render_template('pages/home.html')
        except:
            flash(
              'An error occurred. artist ' +
              data['name'] +
              ' could not be listed.')
            return render_template('errors/500.html')
    else:
      flash(form.errors)
      return redirect(url_for('create_artist_form'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    try:
        show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')).join(Artist).join(Venue).all()
        return render_template('pages/shows.html', shows=show)
    except:
        return render_template('errors/500.html')

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    try:
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)
    except:
        return render_template('errors/500.html')

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:    
        data = request.form
        form = ShowForm(data, csrf_enabled=False)
        if form.validate():
            aid=data['artist_id']
            vid=data['venue_id']
            checka = Artist.query.get(aid)
            checkb = Venue.query.get(vid)
            if(checka and checkb):
                
                sho = Shows(
                    Artist_id=data['artist_id'],
                    Venue_id=data['venue_id'],
                    start_time=data['start_time'])
                db.session.add(sho)
                db.session.commit()
                flash(
                    'show ' +
                    data['artist_id'] +
                    data['venue_id'] +
                    data['start_time'] +
                    ' was successfully listed!')
                db.session.close()
                return redirect(url_for('index'))
        
            else:
                flash('the ids should be valied')
                return redirect(url_for('create_shows'))
        else:
            flash(form.errors)
            return redirect(url_for('create_shows'))
    except:
        flash('An error occurred. the new show could not be listed.')
        return render_template('errors/500.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
