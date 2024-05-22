import uuid
import hashlib

import database
import models

def token_is_valid(guid):
    try:
        get_current_user(guid)
        return True
    except:
        return False

def generate_token():
    return uuid.uuid4()

def hash_password(password):
    salt = 'onomatopeja'
    new_password = password + salt
    return hashlib.md5(new_password.encode()).hexdigest()

def get_current_user(guid):
    token = database.get_token(guid)
    return database.get_user_by_id(token.user_id)

def register(user):
    try:
        try:
            database.get_user_by_username(user.username)
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
        user = database.get_user_by_username(username)
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

def get_ships(guid):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    return database.get_ships()

def get_ship(guid, id):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    return database.get_ship(id)

def get_ship_location(guid, id):
    #TODO: implement properly
    return

def book_ship(guid, id):
    #TODO: implement properly
    return

def get_booked_ships(guid):
    #TODO: implement properly
    return

def receive_messages(guid):
    #TODO: implement properly
    return

def send_message(guid, message):
    #TODO: implement properly
    return

def add_ship(guid, ship):
    #TODO: implement properly
    return

def update_ship(guid, ship):
    #TODO: implement properly
    return

def delete_ship(guid, id):
    #TODO: implement properly
    return