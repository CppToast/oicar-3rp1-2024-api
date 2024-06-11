import pyodbc
import datetime

import models

DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = '192.168.88.97'
DATABASE = 'PrachtYacht'
USERNAME = 'sa'
PASSWORD = 'Oicarbaza123'

connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
print("Connecting to database...")
conn = pyodbc.connect(connectionString)
print("Connected!")

cursor = conn.cursor()

def commit():
    global cursor
    cursor.execute("COMMIT")

def call_procedure(name, params = []):
    global cursor
    if params != []:
        params_template = ''
        for i in range(len(params)):
            params_template += '?'
            if i < len(params) - 1:
                params_template += ', '
        cursor.execute(f"{{CALL {name} ({params_template})}}", params)
    else:
        cursor.execute(f"{{CALL {name}}}", params)

def find_by_id(list, id):
    for i in list:
        if i[0] == id:
            return i
    return None


# User
def get_user_by_id(id):
    global cursor
    call_procedure('SelectSingleRegisteredUser', [id])
    rows = cursor.fetchall()

    id, email, username, passwordhash, renter = rows[0]
    return models.User(id, email, username, passwordhash, renter)

def get_user_by_username(username):
    global cursor
    call_procedure('SelectSingleRegisteredUserByUsername', [username])
    rows = cursor.fetchall()

    id, email, username, passwordhash, renter = rows[0]
    return models.User(id, email, username, passwordhash, renter)

def get_user_by_email(email):
    global cursor
    call_procedure('SelectSingleRegisteredUserByEmail', [email])
    rows = cursor.fetchall()
    
    id, email, username, passwordhash, renter = rows[0]
    return models.User(id, email, username, passwordhash, renter)

def register_user(user):
    global cursor
    call_procedure('InsertRegisteredUser', [user.email, user.username, user.passwordhash, user.renter])
    commit()


# Token
def get_token(guid):
    global cursor
    call_procedure('SelectSingleActiveToken', [guid])
    rows = cursor.fetchall()

    id, user_id, guid = rows[0]
    return models.Token(id, user_id, guid)

def register_token(user_id, guid):
    global cursor
    call_procedure('InsertActiveToken', [user_id, guid])
    commit()
    return get_token(guid)

def unregister_token(token):
    global cursor
    call_procedure('DeleteActiveToken', [token.id])
    commit()

# Location
def get_location(id):
    global cursor
    call_procedure('SelectSingleLocation', [id])
    rows = cursor.fetchall()

    id, name = rows[0]
    return name

def get_location_id(name):
    global cursor
    call_procedure('SelectSingleLocationByName', [name])
    rows = cursor.fetchall()

    id, name = rows[0]
    return id

def create_location(name):
    global cursor
    call_procedure('InsertLocation', [name])
    commit()

def get_or_create_location_id(name):
    global cursor
    try:
        return get_location_id(name)
    except:
        create_location(name)
        return get_location_id(name)

# Route
def get_route(start_id):
    global cursor
    route = []
    call_procedure('SelectRoute')
    all_routes = cursor.fetchall()
    while True:
        current_route = find_by_id(all_routes, start_id)
        location = get_location(current_route[1])
        route.append(location)
        start_id = current_route[2]
        if start_id == None:
            break
    return route

def create_route(locations):
    call_procedure('SelectRoute')
    all_routes = cursor.fetchall()
    start_id = 1
    for i in all_routes:
        if i[0] > start_id: start_id = i[0]
    start_id += 1

    for i in range(start_id, start_id + len(locations)):
        location_id = get_or_create_location_id(locations[i - start_id])
        call_procedure('InsertRoute', [i, location_id, None])
        if i > start_id:
            call_procedure('UpdateRoute', [i - 1, location_id, i])
    
    commit()
    return start_id

# Equipment
def get_equipment(id):
    global cursor
    call_procedure('SelectSingleEquipment', [id])
    rows = cursor.fetchall()

    id, name = rows[0]
    return name

def get_equipment_id(name):
    global cursor
    call_procedure('SelectSingleEquipmentByName', [name])
    rows = cursor.fetchall()

    id, name = rows[0]
    return id

def create_equipment(name):
    global cursor
    call_procedure('InsertEquipment', [name])
    commit()

def get_or_create_equipment_id(name):
    global cursor
    try:
        return get_equipment_id(name)
    except:
        create_equipment(name)
        return get_equipment_id(name)

# Crew
def get_crew(id):
    global cursor
    call_procedure('SelectSingleCrewRole', [id])
    rows = cursor.fetchall()

    id, name = rows[0]
    return name

def get_crew_id(name):
    global cursor
    call_procedure('SelectSingleCrewRoleByName', [name])
    rows = cursor.fetchall()

    id, name = rows[0]
    return id

def create_crew(name):
    global cursor
    call_procedure('InsertCrewRole', [name])
    commit()

def get_or_create_crew_id(name):
    global cursor
    try:
        return get_crew_id(name)
    except:
        create_crew(name)
        return get_crew_id(name)

# Ship
def get_ships():
    global cursor
    call_procedure('SelectShip')
    rows = cursor.fetchall()
    ships = []
    for row in rows:
        id = row[0]
        ships.append(get_ship(id))
    return ships

def get_ship(id):
    global cursor
    call_procedure('SelectSingleShip', [id])
    rows = cursor.fetchall()
    data = rows[0]

    ship_id = data[0]

    owner_id = data[1]
    owner = get_user_by_id(owner_id).username
    
    type = data[2]
    length = data[3]
    berths = data[4]
    bathrooms = data[5]
    
    equipment = []
    call_procedure('SelectShipEquipment')
    all_equipment = cursor.fetchall()
    for i in all_equipment:
        if i[1] == ship_id:
            equipment.append(get_equipment(i[2]))

    crew = []
    call_procedure('SelectShipCrewRole')
    all_crew = cursor.fetchall()
    for i in all_crew:
        if i[1] == ship_id:
            crew.append(get_crew(i[2]))
    
    route_id = data[6]
    route = get_route(route_id)
    
    return models.Ship(id, owner, type, length, berths, bathrooms, equipment, crew, route)

def create_ship(ship):
    global cursor

    route_id = create_route(ship.route)

    call_procedure('InsertShip', [
        get_user_by_username(ship.owner).id,
        ship.type,
        ship.length,
        ship.berths,
        ship.bathrooms,
        route_id
    ])
    commit()
    # ship_id = cursor.fetchall()

    # Do not ask how, do not ask why, because I cannot answer those questions.
    # For some indecipherable reason, having a SELECT statement inside a 
    # procedure does not make it a query, and pyodbc seemingly cannot fetch 
    # the result said SELECT statement returns.
    # 
    # As a result of said behavior, after spending literal hours trying to
    # debug this issue I'm forced to do this dumb hack and pray to God that it 
    # works and doesn't completely screw up everything.

    call_procedure('SelectShip')
    all_ships = cursor.fetchall()

    ship_id = 0
    for i in all_ships:
        if i[0] > ship_id: ship_id = i[0]

    # Hack over. I sincerely apologize for the horror your eyes had to witness.

    for i in ship.equipment:
        assign_equipment_to_ship(i, ship_id)
    
    for i in ship.crew:
        assign_crew_to_ship(i, ship_id)
    
    return ship_id
    

# Links
def assign_equipment_to_ship(equipment, ship_id):
    equipment_id = get_or_create_equipment_id(equipment)
    call_procedure('InsertShipEquipment', [ship_id, equipment_id])
    commit()

def assign_crew_to_ship(crew, ship_id):
    crew_id = get_or_create_crew_id(crew)
    call_procedure('InsertShipCrewRole', [ship_id, crew_id])
    commit()

# Messages
def send_message(sender_id, recipient_id, body):
    timestamp = datetime.datetime.now()
    call_procedure('InsertMessage', [sender_id, recipient_id, timestamp, body])
    commit()

def get_new_messages(recipient_id):
    call_procedure('SelectUndeliveredMessages', [recipient_id])
    data = cursor.fetchall()
    messages = []
    ids = []
    for i in data:
        sender = i[1]
        recipient = i[2]
        body = i[3]
        timestamp = i[5]
        messages.append(Message(sender, recipient, timestamp, body))

        ids.append(i[0])
    
    for i in ids:
        mark_message_as_delivered(i)
    
    return messages

def mark_message_as_delivered(message_id):
    call_procedure('MarkMessagesAsDelivered', [message_id])
    commit()