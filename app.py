'''
IMPORTS
'''
from flask import Flask, render_template, request, g
import requests
from random import randint
import sqlite3

# flask app
app = Flask(__name__)

'''
CONSTANTS
'''

# DATABASE
DATABASE = 'cat_database.db'

# API KEYS
BASE_URL = 'https://api.flickr.com/services/rest/'
METHOD = 'flickr.photos.search'
# API_KEY = '430f7acd5b6fd9cb84c8b6c736e56d7e'
API_KEY = '690218c5f747a9d3cce5fdfe62b8cf50'
TAGS = 'cats'
EXTRAS = 'url_m'
FORMAT = 'json'
NOJSONCALLBACK = '1'
AUTH_TOKEN = '72157670486559662-b5cf454d32ef17e9'
API_SIG = 'd3139c45cb84feace2c849c7780c431b'

payload = {'method': METHOD,
           'api_key': API_KEY,
           'tags': TAGS,
           'extras': EXTRAS,
           'format': FORMAT,
           'nojsoncallback': NOJSONCALLBACK}
        #    'auth_token': AUTH_TOKEN,
        #    'api_sig': API_SIG}

# RESPONSE KEYS
DATA = 'photos'
PHOTO_LIST = 'photo'
URL = 'url_m'

'''
ROUTES
'''

@app.route('/')
def index():
    r = requests.get(BASE_URL, params=payload)

    json_response = r.json()
    json_data = json_response[DATA]
    json_photo_list = json_data[PHOTO_LIST]

    # photo_url = json_photo_list[0][URL]
    num_photos = len(json_photo_list)
    random_index_1 = randint(0, num_photos-1)
    random_index_2 = randint(0, num_photos-1)
    while random_index_1 == random_index_2:
        random_index_2 = randint(0, num_photos-1)

    photo_dicts = [json_photo_list[random_index_1],
                   json_photo_list[random_index_2]]

    return render_template('index.html',
                           photo_dicts=photo_dicts)

@app.route('/', methods=['POST'])
def more_cats():
    image_id = request.form['id']
    image_secret = request.form['secret']
    image_url = request.form['url_m']
    my_values = (image_id, image_secret, image_url)
    my_fields = ('image_id', 'image_secret', 'image_url')
    insert('cat_picks', my_fields, my_values)
    return index()

@app.route('/top_cat/')
def top_cat():
    top_cat_url = ""
    for pick in query_db('select image_url from cat_picks group by image_url order by count(image_url) desc'):
        # my_list.append("{} has the url {}".format(pick['image_id'],
        #                                           pick['image_url']))
        top_cat_url = pick
        break
    # return render_template('top_cat.html', my_list=my_list)
    return render_template('top_cat.html', top_cat_url=top_cat_url)

'''
DB methods
'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert(table, fields=(), values=()):
    # g.db is the database connection
    # cur = g.db.cursor()
    cur = get_db().cursor()
    query = 'INSERT INTO {} ({}) VALUES ({})'.format(
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    # g.db.commit()
    get_db().commit()
    id = cur.lastrowid
    cur.close()
    return id

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
