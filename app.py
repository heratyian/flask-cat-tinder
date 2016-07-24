from flask import Flask, render_template, request
import requests
from random import randint


app = Flask(__name__)

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
    print(request)
    image_id = request.form['id']

    return index()




if __name__ == '__main__':
    app.run(debug=True)
