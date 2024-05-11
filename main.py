#!/usr/bin/env python
# encoding: utf-8
import json
import bs4
import flask

import operations

app = flask.Flask(__name__)


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        flask.abort(404)


@app.route('/')
@app.route('/index')
def index():
    return read_file('endpoints.html')

@app.route('/register')
def register():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/login')
def login():
    #TODO: implement properly
    return read_file('examples/response_login_success.json')

@app.route('/logout')
def logout():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/ships')
def ships():
    #TODO: implement properly
    return read_file('examples/response_ships_success.json')

@app.route('/ships/<id>')
def ships_id(id):
    #TODO: implement properly
    return read_file('examples/response_singleship_success.json')

@app.route('/bookShip/<id>')
def book_ship(id):
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/bookedShips')
def booked_ships():
    #TODO: implement properly
    return read_file('examples/response_ships_success.json')

@app.route('/receiveMessages')
def receive_messages():
    #TODO: implement properly
    return read_file('examples/response_messagereceive_success.json')

@app.route('/sendMessage')
def send_message():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/addShip')
def add_ship():
    #TODO: implement properly
    return '{ "success": true, "id": 0 }'

@app.route('/updateShip')
def update_ship():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/deleteShip/<id>')
def delete_ship(id):
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')


app.run(host='0.0.0.0')
