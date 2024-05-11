import pyodbc 

SERVER = '192.168.1.97'
DATABASE = 'PrachtYacht'
USERNAME = 'sa'
PASSWORD = 'Oicarbaza123'

connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

cursor = conn.cursor()
cursor.execute('SELECT * FROM Persons')

for row in cursor:
    print('row = %r' % (row,))