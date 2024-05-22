#!/usr/bin/env python
# encoding: utf-8
import json
import bs4
import flask

import operations
import models

app = flask.Flask(__name__)


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        flask.abort(500)


@app.route('/')
@app.route('/index')
def index():
    return read_file('endpoints.html')

@app.route('/register', methods = ['POST'])
def register():
    try:
        content = flask.request.json
        email = content['email']
        username = content['username']
        password = content['password']
        renter = content['renter']
        user = models.User(-1, email, username, password, renter)
        ret = operations.register(user)
        return flask.jsonify(ret), 400 if ret['success'] == False else 200
    except:
        return read_file('examples/response_generic_fail.json'), 400

@app.route('/login', methods = ['POST'])
def login():
    # try:
        content = flask.request.json
        username = content['username']
        password = content['password']
        ret = operations.login(username, password)
        if ret['success'] == False: raise Exception('Operation failed!')
        return flask.jsonify(ret)
    # except:
        return read_file('examples/response_generic_fail.json'), 400

@app.route('/logout', methods = ['POST'])
def logout():
    try:
        content = flask.request.json
        token = content['token']
        ret = operations.logout(token)
        if ret['success'] == False: raise Exception('Operation failed!')
        return flask.jsonify(ret)
    except:
        return read_file('examples/response_generic_fail.json'), 400

@app.route('/ships', methods = ['POST'])
def ships():
    # try:
        content = flask.request.json
        token = content['token']
        try:
            ret = operations.get_ships(token)
            return flask.jsonify(ret)
        except PermissionError as ex:
            return read_file('examples/response_generic_fail.json'), 403
    # except:
    #     return read_file('examples/response_generic_fail.json'), 400

@app.route('/ships/<id>', methods = ['POST'])
def ships_id(id):
    try:
        content = flask.request.json
        token = content['token']
        try:
            ret = operations.get_ship(token, id)
            return flask.jsonify(ret)
        except PermissionError as ex:
            return read_file('examples/response_generic_fail.json'), 403
    except:
        return read_file('examples/response_generic_fail.json'), 400

@app.route('/bookShip/<id>', methods = ['POST'])
def book_ship(id):
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/bookedShips', methods = ['POST'])
def booked_ships():
    #TODO: implement properly
    return read_file('examples/response_ships_success.json')

@app.route('/receiveMessages', methods = ['POST'])
def receive_messages():
    #TODO: implement properly
    return read_file('examples/response_messagereceive_success.json')

@app.route('/sendMessage', methods = ['POST'])
def send_message():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/addShip', methods = ['POST'])
def add_ship():
    #TODO: implement properly
    return '{ "success": true, "id": 0 }'

@app.route('/updateShip', methods = ['POST'])
def update_ship():
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')

@app.route('/deleteShip/<id>', methods = ['POST'])
def delete_ship(id):
    #TODO: implement properly
    return read_file('examples/response_generic_success.json')


app.run(host='0.0.0.0')
