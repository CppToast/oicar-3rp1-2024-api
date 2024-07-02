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

def user_is_renter(guid):
    try:
        user = get_current_user(guid)
        return user.renter
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
        raise Exception('Operation failed!')

def logout(guid):
    try:
        token = database.get_token(guid)
        database.unregister_token(token)
        return {'success': True}
    except:
        raise Exception('Operation failed!')

def get_ships(guid):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    return database.get_ships()

def get_ship(guid, id):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    return database.get_ship(id)

def get_ship_location(guid, id):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    
    # This is where we would communicate with the ship's GPS and determine the
    # location, but since we're faking it, might as well fake it here. No need
    # to store it to the DB.
    
    return {
        "success": True,
        'latitude': 43.645218,
        'longitude': 15.194806
    }

def book_ship(guid, id):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    user = get_current_user(guid)
    try:
        database.book_ship(user.id, id)
        return {'success': True}
    except:
        raise Exception('Operation failed!')

def get_booked_ships(guid):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    user = get_current_user(guid)
    return database.get_booked_ships(user.id)

def receive_messages(guid):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    user = get_current_user(guid)
    return database.get_new_messages(user)

def send_message(guid, recipient, body):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    try:
        sender_id = get_current_user(guid)
        recipient_id = database.get_user_by_username(recipient).id
        database.send_message(sender_id, recipient_id, body)
        return {'success': True}
    except:
        raise Exception('Operation failed!')

def add_ship(guid, ship):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    if not user_is_renter(guid): raise PermissionError('Permission denied!')
    try:
        ship.owner = get_current_user(guid).username
        ship_id = database.create_ship(ship)
        return {'success': True, 'id': ship_id}
    except:
        raise Exception('Operation failed!')

def update_ship(guid, ship):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    if not user_is_renter(guid): raise PermissionError('Permission denied!')
    try:
        ship.owner = get_current_user(guid).username
        database.update_ship(ship)
        return {'success': True}
    except:
        raise Exception('Operation failed!')

def delete_ship(guid, id):
    if not token_is_valid(guid): raise PermissionError('Invalid token!')
    if not user_is_renter(guid): raise PermissionError('Permission denied!')
    try:
        database.delete_ship(id)
        return {'success': True}
    except:
        raise Exception('Operation failed!')