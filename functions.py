from models import db, Artist , Venue ,Shows 
from datetime import datetime



# functions using the join queries -------------------------------------------
def upArtistShows(id):
    show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')
    ).join(Artist).join(Venue).filter(Shows.start_time>str(datetime.now()),Artist.id==id).all()
    return show

def pastArtistShows(id):
    show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')
    ).join(Artist).join(Venue).filter(Shows.start_time<str(datetime.now()),Artist.id==id).all()
    return show


def upVenueShows(id):
    show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')
    ).join(Artist).join(Venue).filter(Shows.start_time>str(datetime.now()),Venue.id==id).all()
    return show

def upVShows(id):
    show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')
    ).join(Artist).join(Venue).filter(Shows.start_time>str(datetime.now()),Venue.id==id).all()
    return show


def pastVShows(id):
    show=db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Shows.start_time.label('start_time')
    ).join(Artist).join(Venue).filter(Shows.start_time<str(datetime.now()),Venue.id==id).all()
    return show
  

  ##------------------------------

def getvenuesort():  #unused method
    Shows.query.join(Venue).with_entities(
        Shows.Venue_id, Venue.name).order_by(
        Shows.Venue_id).all()

# Artist search -----------------------------
def search(id):
    key = '%' + id + '%'  # TEST
    
    artists = Artist.query.filter(Artist.name.ilike(key)).all()
    count = len(artists)
    for artist in artists:
        artist.num_upcoming_shows = len(upArtistShows(artist.id))
    data = {
        "count": count,
        "data": artists
    }
    return data


# venue search---------------------------------------------------------
def search2(key2):
    key = '%' + key2 + '%'

    venues = Venue.query.filter(Venue.name.ilike(key)).all()
    count = len(venues)
    data = []
    for venue in venues:
        beta = {
            "id": venue.id, 
            "name": venue.name,
            "num_upcoming_shows": len(upVenueShows(venue.id))
        }
        data.append(beta)
    response = {
        "count": count,
        "data": data
    }
    return response




#counts venues in specific cities returns the venues grouped by cities---------------------------------
def countvins():
    citylist = Venue.query.distinct(Venue.city).all()
    data = []
    for city in citylist:
        tcity = city.city
        state = city.state
        venuelist = Venue.query.filter_by(city=tcity).all()
        venues = []
        for ven in venuelist:
            id = ven.id
            name = ven.name
            upcoming = len(upVenueShows(id))
            venue = {
                "id": id,
                "name": name,
                "num_upcoming_shows": upcoming
            }
            venues.append(venue)
        predata = {
            "city": tcity,
            "state": state,
            "venues": venues
        }
        data.append(predata)
    return data


#unused mehtod----------------------------------------------
def getgenres(id, isvenue):
    if isvenue:
        vs = Venue.query.get(id)
        genlist = vs.genres.split(',')
        return genlist
    else:
        vs = Artist.query.get(id)
        genlist = vs.genres.split(',')
        return genlist

#search for venue -------------------------------------------------------------
def getvenue(id):
    try:  
        ven = Venue.query.get(id)
        uplist = upVShows(id)
        downlist = pastVShows(id)
        data = {
            "id": id,
            "name": ven.name,
            "genres": getgenres(id, True),
            "address": ven.address,
            "city": ven.city,
            "state": ven.state,
            "phone": ven.phone,
            "website": ven.website,
            "facebook_link": ven.facebook_link,
            "seeking_talent": ven.seeking_talent,
            "seeking_description": ven.seeking_description,
            "image_link": ven.image_link,
            "past_shows": downlist,
            "upcoming_shows": uplist,
            "past_shows_count": len(downlist),
            "upcoming_shows_count": len(uplist),
        }
        return data
    except BaseException:
        return {}

#search for and artist returning relevant data---------------------------------------------
def artistsearch(id):  
    artist = Artist.query.get(id)
    upshows = upArtistShows(id)
    pastshows = pastArtistShows(id)
    gen = artist.genres
    artist.genres = gen.split(',')
    artist.past_shows = pastshows
    artist.past_shows_count = len(pastshows)
    artist.upcoming_shows = upshows
    artist.upcoming_shows_count = len(upshows)
    return artist