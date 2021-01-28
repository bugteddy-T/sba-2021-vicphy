# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, render_template, request
from modules.cbf_test import *
from modules.place import *
from modules.photo import *
import os
import random

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# http://ogamxseoul.appspot.com/


# bg_1.jpg source: https://pixabay.com/ko/photos/%ED%95%9C%EA%B0%95-%EC%84%9C%EC%9A%B8-%EA%B0%95-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD-3845034/
# bg_2.jpg source: https://pixabay.com/ko/photos/%ED%95%9C%EA%B0%95-%EC%84%9C%EC%9A%B8-%EB%85%B8%EC%9D%84-%ED%95%98%EB%8A%98-%EC%95%BC%EA%B2%BD-3804298/
# bg_3.jpg source: google
# bg_4.jpg source: https://pixabay.com/ko/photos/%EC%84%9C%EC%9A%B8-%EC%97%AC%EC%9D%98%EB%8F%84-%ED%95%98%EB%8A%98-%EA%B5%AC%EB%A6%84-410265/
@app.route('/')
def index():
    image_list = ['bg_1.jpg', 'bg_2.jpg', 'bg_3.jpg', 'bg_4.jpg']
    image_file = image_list[random.randint(0, len(image_list) - 1)]
    return render_template('index.html', image_file = image_file)


# 13번 사진 변경 source: https://pixabay.com/ko/photos/%EC%82%BC%EA%B2%B9%EC%82%B4-%EA%B3%A0%EA%B8%B0-%EA%B5%AC%EC%9D%B4-%EB%8F%BC%EC%A7%80%EA%B3%A0%EA%B8%B0-5731404/
# 19번 사진 변경 source: https://pixabay.com/ko/photos/%EC%95%BC%EA%B2%BD-%EC%84%9C%EC%9A%B8-korea-%ED%95%9C%EA%B0%95-3538984/
@app.route('/ogam')
def ogam():
    photos = get_photos(sqlite_path="static/data/photos.sqlite")
    per_row = 3
    return render_template('ogam.html', photos = photos, rows = int(len(photos)/per_row))


@app.route('/seoul')
def seoul():
    parameter_dict = request.args.to_dict()
    print(parameter_dict['ogamId'])
    photo_id_list = parameter_dict['ogamId'].split(',')
    print(photo_id_list)
    get_tag_data(sqlite_path="static/data/photos.sqlite", photo_id_list=photo_id_list)
    return render_template('seoul.html')


@app.route('/test/photos')
def test_photos():
    photos = get_photos("static/data/photos.sqlite")
    return render_template('photos.html', photos = photos)


@app.route('/test/places')
def test_places():
    places = get_places("./data/placelist-v.1.2.xlsx")
    return render_template('places.html', places = places)


@app.route('/test/map')
def test_map():
    parameter_dict = request.args.to_dict()
    api_key = os.getenv('KAKAO_MAP_API_KEY')
    place = get_place_by_id("./data/placelist-v.1.2.xlsx", int(parameter_dict['place_id']))
    return render_template('map.html', api_key = api_key, place = place)


'''
@app.route('/test/cbf')
def cbf():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        places = get_places_id_place("./data/place-data-tag.csv")
        return render_template('cbf.html', places = places)
    else:
        places = recommend_places("./data/place-data-tag.csv", int(parameter_dict['place_id']))
        print(places)
        return render_template('cbf-result.html', places = places)
'''


@app.errorhandler(404)
def page_not_found(error):
     return render_template('page-not-found.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
     return render_template('internal-server-error.html'), 500


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
