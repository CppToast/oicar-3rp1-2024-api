import pyodbc
import models

DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = '192.168.1.97'
DATABASE = 'PrachtYacht'
USERNAME = 'sa'
PASSWORD = 'Oicarbaza123'

connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

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


# User
def get_user(username):
    global cursor
    call_procedure('SelectSingleRegisteredUser', [username])
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


