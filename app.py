import time

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import Model

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
model = Model()
cities = ["Boston", "Seattle", "New York", "Chicago", "San Francisco"]
open_weather_key = "207e19459d3c8a3b9350554022c23635"
url = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_info(cities):
    weather_info = {}
    for city in cities:
        params = {'q': city, 'appid': "207e19459d3c8a3b9350554022c23635"}
        response = requests.get(url=url, params=params)
        data = response.json()

        for val in data['weather']:
            temp = int(data['main']['temp'])
            temp = (temp - 273.15) * 9 / 5 + 32
            temp = round(temp, 1)
            description = str(temp) + u'\N{DEGREE SIGN}F' + ' | ' + val['main'] + ', ' + val['description']
            weather_info[city] = description

    return weather_info


start_time = int(time.time())
expiry = 10 * 60
weather_of_cities = get_weather_info(cities)


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def get_weather_description(city):
    global start_time, weather_of_cities
    curr_time = int(time.time())
    if curr_time - start_time >= expiry:
        start_time = curr_time
        weather_of_cities = get_weather_info(cities)

    return weather_of_cities[city]


def add_weather(items):
    items_with_weather = []
    for item in items:
        city = item['location']
        description = get_weather_description(city)
        item['weather'] = description
        items_with_weather.append(item)

    return items_with_weather


@app.route('/items', methods=['GET'])
def api_list():
    items = model.list()
    items_with_weather = add_weather(items)
    return jsonify(items_with_weather)


@app.route('/items/<item_id>', methods=['GET'])
def api_get(item_id):
    if not item_id:
        raise InvalidAPIUsage("No item id provided!")

    item = model.get(item_id)

    if not item:
        raise InvalidAPIUsage("No such item!", status_code=404)
    return jsonify(item)


@app.route('/items/add', methods=['POST'])
def api_insert():
    item = request.get_json()

    if not item:
        raise InvalidAPIUsage("No item provided!")

    if 'name' not in item or 'location' not in item:
        raise InvalidAPIUsage("Missing parameter")

    if not item['name'] or not item['location']:
        raise InvalidAPIUsage("Missing parameter")

    if item['location'] not in cities:
        raise InvalidAPIUsage("Only allow Boston, Seattle, New York, Chicago, or San Francisco")

    return jsonify(model.insert(item))


@app.route('/items/edit', methods=['PUT'])
def api_edit():
    item = request.get_json()

    if not item:
        raise InvalidAPIUsage("No item provided!")

    if 'item_id' not in item or 'name' not in item or 'location' not in item:
        raise InvalidAPIUsage("Missing parameter")

    if not item['item_id'] or not item['name'] or not item['location']:
        raise InvalidAPIUsage("Missing parameter")

    if item['location']:
        if item['location'] not in cities:
            raise InvalidAPIUsage("Only allow Boston, Seattle, New York, Chicago, or San Francisco")

    return jsonify(model.edit(item))


@app.route('/items/delete/<item_id>', methods=['DELETE'])
def api_delete(item_id):
    if not item_id:
        raise InvalidAPIUsage("No item id provided!")

    return jsonify(model.delete(item_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
