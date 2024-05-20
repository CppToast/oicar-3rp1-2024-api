import uuid
import hashlib

import database
import models

# https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict
# https://stackoverflow.com/questions/45412228/sending-json-and-status-code-with-a-flask-response
# convert dataclass to dict, then dict to json
# what about reverse?

def token_is_valid(guid):
    try:
        database.get_token(guid)
        return True
    except:
        return False

def generate_token():
    return uuid.uuid4()

def hash_password(password):
    salt = 'onomatopeja'
    new_password = password + salt
    return hashlib.md5(new_password.encode()).hexdigest()

def register(user):
    try:
        try:
            database.get_user(user.username)
            return {'success': False, 'reason': 'username_taken'}
        except: pass 

        try:
            database.get_user_by_email(user.email)
            return {'success': False, 'reason': 'email_taken'}
        except: pass

        user.passwordhash = hash_password(user.passwordhash)
        database.register_user(user)
        return {'success': True}
    except:
        return {'success': False, 'reason': 'internal_error'}

def login(username, password):
    try:
        user = database.get_user(username)
        if user.passwordhash != hash_password(password): raise Exception('Invalid password!')

        token = database.register_token(user.id, generate_token())
        return {'success': True, 'token': token.guid}
    except:
        return {'success': False}

def logout(guid):
    try:
        token = database.get_token(guid)
        database.unregister_token(token)
        return {'success': True}
    except:
        return {'success': False}

def get_ships(token):
    #TODO: implement properly
    return

def get_ship(token, id):
    #TODO: implement properly
    return

def get_ship_location(token, id):
    #TODO: implement properly
    return

def book_ship(token, id):
    #TODO: implement properly
    return

def get_booked_ships(token):
    #TODO: implement properly
    return

def receive_messages(token):
    #TODO: implement properly
    return

def send_message(token, message):
    #TODO: implement properly
    return

def add_ship(token, ship):
    #TODO: implement properly
    return

def update_ship(token, ship):
    #TODO: implement properly
    return

def delete_ship(token, id):
    #TODO: implement properly
    return