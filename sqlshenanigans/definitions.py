class Table:
    def __init__(self, name, columns):
        self.name = table_name
        self.columns = columns

database_name = "PrachtYacht"

tables = []



table_name = "RegisteredUser"
columns = [
    ("IDUser", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("Email", "nvarchar(50)", []),
    ("Username", "nvarchar(50)", []),
    ("PasswordHash", "nvarchar(50)", []),
    ("IsRenter", "bit", []),
]
tables.append(Table(table_name, columns))

table_name = "ActiveToken"
columns = [
    ("IDActiveToken", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("UserID", "int", ["FOREIGN KEY REFERENCES RegisteredUser(IDUser)"]),
    ("GUID", "nvarchar(36)", []),
]
tables.append(Table(table_name, columns))

table_name = "Location"
columns = [
    ("IDLocation", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("Name", "nvarchar(50)", []),
]
tables.append(Table(table_name, columns))

table_name = "Route"
columns = [
    ("IDRoute", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("LocationID", "int", ["FOREIGN KEY REFERENCES Location(IDLocation)"]),
    ("NextRouteID", "int", ["FOREIGN KEY REFERENCES Route(IDRoute)"]),
]
tables.append(Table(table_name, columns))

table_name = "Ship"
columns = [
    ("IDShip", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("OwnerID", "int", ["FOREIGN KEY REFERENCES RegisteredUser(IDUser)"]),
    ("Type", "nvarchar(50)", []),
    ("Length", "float", []),
    ("Berths", "int", []),
    ("Bathrooms", "int", []),
    ("RouteID", "int", ["FOREIGN KEY REFERENCES Route(IDRoute)"]),
]
tables.append(Table(table_name, columns))

table_name = "Equipment"
columns = [
    ("IDEquipment", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("Name", "nvarchar(50)", []),
]
tables.append(Table(table_name, columns))

table_name = "ShipEquipment"
columns = [
    ("IDShipEquipment", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("ShipID", "int", ["FOREIGN KEY REFERENCES Ship(IDShip)"]),
    ("EquipmentID", "int", ["FOREIGN KEY REFERENCES Equipment(IDEquipment)"]),
]
tables.append(Table(table_name, columns))

table_name = "CrewRole"
columns = [
    ("IDCrewRole", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("Name", "nvarchar(50)", []),
]
tables.append(Table(table_name, columns))

table_name = "ShipCrewRole"
columns = [
    ("IDShipCrewRole", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("ShipID", "int", ["FOREIGN KEY REFERENCES Ship(IDShip)"]),
    ("CrewRoleID", "int", ["FOREIGN KEY REFERENCES CrewRole(IDCrewRole)"]),
]
tables.append(Table(table_name, columns))

table_name = "CurrentLocation"
columns = [
    ("IDCurrentLocation", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("ShipID", "int", ["FOREIGN KEY REFERENCES Ship(IDShip)"]),
    ("Latitude", "float", []),
    ("Longitude", "float", []),
]
tables.append(Table(table_name, columns))

table_name = "Booking"
columns = [
    ("IDBooking", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("UserID", "int", ["FOREIGN KEY REFERENCES RegisteredUser(IDUser)"]),
    ("ShipID", "int", ["FOREIGN KEY REFERENCES Ship(IDShip)"]),
]
tables.append(Table(table_name, columns))

table_name = "Message"
columns = [
    ("IDMessage", "int", ["PRIMARY KEY", "IDENTITY(1,1)"]),
    ("SenderID", "int", ["FOREIGN KEY REFERENCES RegisteredUser(IDUser)"]),
    ("RecipientID", "int", ["FOREIGN KEY REFERENCES RegisteredUser(IDUser)"]),
    ("Body", "nvarchar(200)", []),
    ("Timestamp", "datetime", []),
    ("IsDelivered", "bit", []),
]
tables.append(Table(table_name, columns))