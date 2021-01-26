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
from modules.CBF import recommend_places, get_place_list

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# http://places4you.appspot.com/


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cbf')
def cbf():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        place_list = get_place_list("./data/place-data-tag.csv")
        return render_template('cbf.html', place_list = place_list)
    else:
        place_list = recommend_places("./data/place-data-tag.csv", int(parameter_dict['place_id']))
        print(place_list)
        return render_template('cbf-result.html', place_list = place_list)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
