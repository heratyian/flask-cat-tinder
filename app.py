from flask import Flask, render_template, request
import requests


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
    # r = requests.get('https://api.flickr.com/services/rest/?method=\
    #                   flickr.photos.search&api_key=430f7acd5b6fd9cb\
    #                   84c8b6c736e56d7e&tags=pokemon&extras=url_m&fo\
    #                   rmat=json&nojsoncallback=1&auth_token=7215767\
    #                   0486559662-b5cf454d32ef17e9&api_sig=d3139c45c\
    #                   b84feace2c849c7780c431b')
    r = requests.get(BASE_URL, params=payload)

    json_response = r.json()
    json_data = json_response[DATA]
    json_photo_list = json_data[PHOTO_LIST]

    photo_url = json_photo_list[0][URL]
    photo_urls = [json_photo_list[1][URL], json_photo_list[2][URL]]

    return render_template('index.html',
                           photo_url=photo_url,
                           photo_urls=photo_urls)

if __name__ == '__main__':
    app.run()
