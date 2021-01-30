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
from modules.cbf_by_place import get_places_id_place, recommend_places
from modules.place import get_place_by_id, get_places, get_tour_type_data, get_places_by_place_list, get_tour_type_list
from modules.photo import get_photos, get_tag_data
from modules.cbf_by_tag import get_places_by_cbf
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
@app.route('/select')
def select():
    photos = get_photos()
    per_row = 3
    return render_template('select.html', photos = photos, rows = int(len(photos) / per_row))


@app.route('/type')
def select():
    parameter_dict = request.args.to_dict()
    photo_id_list = parameter_dict['id'].split(',')
    tour_type_list = get_tour_type_list()
    return render_template('type.html', id_list = photo_id_list, tour_type_list = tour_type_list)


@app.route('/result')
def result():
    parameter_dict = request.args.to_dict()
    photo_id_list = parameter_dict['id'].split(',')
    tag_data = get_tag_data(photo_id_list)
    print(tag_data)
    keyword = []
    weight = []
    for key in tag_data:
        keyword.append(key)
        weight.append(tag_data[key])
    cbf_data = get_places_by_cbf(keyword, weight)
    tour_type_data = get_tour_type_data(cbf_data['tour_type'])
    places_data1 = get_places_by_place_list(cbf_data['places1'])
    places_data2 = get_places_by_place_list(cbf_data['places2'])
    places_data1_len = len(places_data1)
    places_data2_len = len(places_data2)
    print(tour_type_data)
    return render_template('result.html', tour_type_data = tour_type_data, places_data1 = places_data1, places_data1_len = places_data1_len, places_data2 = places_data2, places_data2_len = places_data2_len)


'''
@app.route('/result')
def result():
    parameter_dict = request.args.to_dict()
    photo_id_list = parameter_dict['id'].split(',')
    tour_type_id_list = get_tour_type_id(photo_id_list)
    print(tour_type_id_list)
    tour_type_text = ["FLEX", "교양", "놀기", "쉬기", "보기", "배우기"]
    tour_type_list = []
    for tour_type_id in tour_type_id_list:
        tour_type = {}
        tour_type['id'] = str(tour_type_id)
        tour_type['text'] = tour_type_text[tour_type_id - 1]
        tour_type_list.append(tour_type)
    print(tour_type_list)
    places_data1 = get_places_by_tour_type(tour_type_list[0]['id'])
    places_data2 = get_places_by_tour_type(tour_type_list[1]['id'])
    return render_template('result.html', tour_type_list = tour_type_list, places_data1 = places_data1, places_data2 = places_data2)
'''


@app.route('/place')
def place():
    parameter_dict = request.args.to_dict()
    api_key = os.getenv('KAKAO_MAP_API_KEY')
    place = get_place_by_id(int(parameter_dict['id']))
    places = recommend_places(int(parameter_dict['id']))
    print(places)
    return render_template('place.html', api_key = api_key, place = place)



@app.route('/test/photos')
def test_photos():
    photos = get_photos()
    return render_template('photos.html', photos = photos)


@app.route('/test/places')
def test_places():
    places = get_places()
    return render_template('places.html', places = places)


@app.route('/test/map')
def test_map():
    parameter_dict = request.args.to_dict()
    api_key = os.getenv('KAKAO_MAP_API_KEY')
    place = get_place_by_id(int(parameter_dict['place_id']))
    return render_template('map.html', api_key = api_key, place = place)


@app.route('/test/cbf')
def cbf():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        places = get_places_id_place()
        return render_template('cbf.html', places = places)
    else:
        places = recommend_places(int(parameter_dict['place_id']))
        print(places)
        return render_template('cbf-result.html', places = places)


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
