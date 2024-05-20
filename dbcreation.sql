USE master
GO
DROP DATABASE IF EXISTS PrachtYacht
GO
CREATE DATABASE PrachtYacht
GO
USE PrachtYacht
GO

--RegisteredUser
--Table Creation SQL:
CREATE TABLE RegisteredUser (
    IDUser int PRIMARY KEY IDENTITY(1,1),
    Email nvarchar(50),
    Username nvarchar(50),
    PasswordHash nvarchar(50),
    IsRenter bit
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertRegisteredUser
    @Email nvarchar(50), @Username nvarchar(50), @PasswordHash nvarchar(50), @IsRenter bit
AS
BEGIN
    INSERT INTO RegisteredUser (Email, Username, PasswordHash, IsRenter)
    VALUES (@Email, @Username, @PasswordHash, @IsRenter);
END;

GO

CREATE PROCEDURE SelectRegisteredUser
AS
BEGIN
    SELECT * FROM RegisteredUser;
END;

GO

CREATE PROCEDURE SelectSingleRegisteredUser
    @Username nvarchar(50)
AS
BEGIN
    SELECT * FROM RegisteredUser
    WHERE Username = @Username;
END;

GO

CREATE PROCEDURE SelectSingleRegisteredUserByEmail
    @Email nvarchar(50)
AS
BEGIN
    SELECT * FROM RegisteredUser
    WHERE Email = @Email;
END;

GO

CREATE PROCEDURE UpdateRegisteredUser
    @IDUser int,
    @Email nvarchar(50), @Username nvarchar(50), @PasswordHash nvarchar(50), @IsRenter bit
AS
BEGIN
    UPDATE RegisteredUser
    SET Email = @Email, Username = @Username, PasswordHash = @PasswordHash, IsRenter = @IsRenter
    WHERE IDUser = @IDUser;
END;

GO

CREATE PROCEDURE DeleteRegisteredUser
    @IDUser int
AS
BEGIN
    DELETE FROM RegisteredUser WHERE IDUser = @IDUser;
END;

GO
--ActiveToken
--Table Creation SQL:
CREATE TABLE ActiveToken (
    IDActiveToken int PRIMARY KEY IDENTITY(1,1),
    UserID int FOREIGN KEY REFERENCES RegisteredUser(IDUser),
    GUID nvarchar(36)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertActiveToken
    @UserID int, @GUID nvarchar(36)
AS
BEGIN
    INSERT INTO ActiveToken (UserID, GUID)
    VALUES (@UserID, @GUID);
END;

GO

CREATE PROCEDURE SelectActiveToken
AS
BEGIN
    SELECT * FROM ActiveToken;
END;

GO

CREATE PROCEDURE SelectSingleActiveToken
    @GUID nvarchar(36)
AS
BEGIN
    SELECT * FROM ActiveToken
    WHERE GUID = @GUID;
END;

GO

CREATE PROCEDURE UpdateActiveToken
    @IDActiveToken int,
    @UserID int, @GUID nvarchar(36)
AS
BEGIN
    UPDATE ActiveToken
    SET UserID = @UserID, GUID = @GUID
    WHERE IDActiveToken = @IDActiveToken;
END;

GO

CREATE PROCEDURE DeleteActiveToken
    @IDActiveToken int
AS
BEGIN
    DELETE FROM ActiveToken WHERE IDActiveToken = @IDActiveToken;
END;

GO
--Location
--Table Creation SQL:
CREATE TABLE Location (
    IDLocation int PRIMARY KEY IDENTITY(1,1),
    Name nvarchar(50)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertLocation
    @Name nvarchar(50)
AS
BEGIN
    INSERT INTO Location (Name)
    VALUES (@Name);
END;

GO

CREATE PROCEDURE SelectLocation
AS
BEGIN
    SELECT * FROM Location;
END;

GO

CREATE PROCEDURE UpdateLocation
    @IDLocation int,
    @Name nvarchar(50)
AS
BEGIN
    UPDATE Location
    SET Name = @Name
    WHERE IDLocation = @IDLocation;
END;

GO

CREATE PROCEDURE DeleteLocation
    @IDLocation int
AS
BEGIN
    DELETE FROM Location WHERE IDLocation = @IDLocation;
END;

GO
--Route
--Table Creation SQL:
CREATE TABLE Route (
    IDRoute int PRIMARY KEY IDENTITY(1,1),
    LocationID int FOREIGN KEY REFERENCES Location(IDLocation),
    NextRouteID int FOREIGN KEY REFERENCES Route(IDRoute)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertRoute
    @LocationID int, @NextRouteID int
AS
BEGIN
    INSERT INTO Route (LocationID, NextRouteID)
    VALUES (@LocationID, @NextRouteID);
END;

GO

CREATE PROCEDURE SelectRoute
AS
BEGIN
    SELECT * FROM Route;
END;

GO

CREATE PROCEDURE UpdateRoute
    @IDRoute int,
    @LocationID int, @NextRouteID int
AS
BEGIN
    UPDATE Route
    SET LocationID = @LocationID, NextRouteID = @NextRouteID
    WHERE IDRoute = @IDRoute;
END;

GO

CREATE PROCEDURE DeleteRoute
    @IDRoute int
AS
BEGIN
    DELETE FROM Route WHERE IDRoute = @IDRoute;
END;

GO
--Ship
--Table Creation SQL:
CREATE TABLE Ship (
    IDShip int PRIMARY KEY IDENTITY(1,1),
    OwnerID int FOREIGN KEY REFERENCES RegisteredUser(IDUser),
    Type nvarchar(50),
    Length float,
    Berths int,
    Bathrooms int,
    RouteID int FOREIGN KEY REFERENCES Route(IDRoute)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertShip
    @OwnerID int, @Type nvarchar(50), @Length float, @Berths int, @Bathrooms int, @RouteID int
AS
BEGIN
    INSERT INTO Ship (OwnerID, Type, Length, Berths, Bathrooms, RouteID)
    VALUES (@OwnerID, @Type, @Length, @Berths, @Bathrooms, @RouteID);
END;

GO

CREATE PROCEDURE SelectShip
AS
BEGIN
    SELECT * FROM Ship;
END;

GO

CREATE PROCEDURE UpdateShip
    @IDShip int,
    @OwnerID int, @Type nvarchar(50), @Length float, @Berths int, @Bathrooms int, @RouteID int
AS
BEGIN
    UPDATE Ship
    SET OwnerID = @OwnerID, Type = @Type, Length = @Length, Berths = @Berths, Bathrooms = @Bathrooms, RouteID = @RouteID
    WHERE IDShip = @IDShip;
END;

GO

CREATE PROCEDURE DeleteShip
    @IDShip int
AS
BEGIN
    DELETE FROM Ship WHERE IDShip = @IDShip;
END;

GO
--Equipment
--Table Creation SQL:
CREATE TABLE Equipment (
    IDEquipment int PRIMARY KEY IDENTITY(1,1),
    Name nvarchar(50)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertEquipment
    @Name nvarchar(50)
AS
BEGIN
    INSERT INTO Equipment (Name)
    VALUES (@Name);
END;

GO

CREATE PROCEDURE SelectEquipment
AS
BEGIN
    SELECT * FROM Equipment;
END;

GO

CREATE PROCEDURE UpdateEquipment
    @IDEquipment int,
    @Name nvarchar(50)
AS
BEGIN
    UPDATE Equipment
    SET Name = @Name
    WHERE IDEquipment = @IDEquipment;
END;

GO

CREATE PROCEDURE DeleteEquipment
    @IDEquipment int
AS
BEGIN
    DELETE FROM Equipment WHERE IDEquipment = @IDEquipment;
END;

GO
--ShipEquipment
--Table Creation SQL:
CREATE TABLE ShipEquipment (
    IDShipEquipment int PRIMARY KEY IDENTITY(1,1),
    ShipID int FOREIGN KEY REFERENCES Ship(IDShip),
    EquipmentID int FOREIGN KEY REFERENCES Equipment(IDEquipment)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertShipEquipment
    @ShipID int, @EquipmentID int
AS
BEGIN
    INSERT INTO ShipEquipment (ShipID, EquipmentID)
    VALUES (@ShipID, @EquipmentID);
END;

GO

CREATE PROCEDURE SelectShipEquipment
AS
BEGIN
    SELECT * FROM ShipEquipment;
END;

GO

CREATE PROCEDURE UpdateShipEquipment
    @IDShipEquipment int,
    @ShipID int, @EquipmentID int
AS
BEGIN
    UPDATE ShipEquipment
    SET ShipID = @ShipID, EquipmentID = @EquipmentID
    WHERE IDShipEquipment = @IDShipEquipment;
END;

GO

CREATE PROCEDURE DeleteShipEquipment
    @IDShipEquipment int
AS
BEGIN
    DELETE FROM ShipEquipment WHERE IDShipEquipment = @IDShipEquipment;
END;

GO
--CrewRole
--Table Creation SQL:
CREATE TABLE CrewRole (
    IDCrewRole int PRIMARY KEY IDENTITY(1,1),
    Name nvarchar(50)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertCrewRole
    @Name nvarchar(50)
AS
BEGIN
    INSERT INTO CrewRole (Name)
    VALUES (@Name);
END;

GO

CREATE PROCEDURE SelectCrewRole
AS
BEGIN
    SELECT * FROM CrewRole;
END;

GO

CREATE PROCEDURE UpdateCrewRole
    @IDCrewRole int,
    @Name nvarchar(50)
AS
BEGIN
    UPDATE CrewRole
    SET Name = @Name
    WHERE IDCrewRole = @IDCrewRole;
END;

GO

CREATE PROCEDURE DeleteCrewRole
    @IDCrewRole int
AS
BEGIN
    DELETE FROM CrewRole WHERE IDCrewRole = @IDCrewRole;
END;

GO
--ShipCrewRole
--Table Creation SQL:
CREATE TABLE ShipCrewRole (
    IDShipCrewRole int PRIMARY KEY IDENTITY(1,1),
    ShipID int FOREIGN KEY REFERENCES Ship(IDShip),
    CrewRoleID int FOREIGN KEY REFERENCES CrewRole(IDCrewRole)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertShipCrewRole
    @ShipID int, @CrewRoleID int
AS
BEGIN
    INSERT INTO ShipCrewRole (ShipID, CrewRoleID)
    VALUES (@ShipID, @CrewRoleID);
END;

GO

CREATE PROCEDURE SelectShipCrewRole
AS
BEGIN
    SELECT * FROM ShipCrewRole;
END;

GO

CREATE PROCEDURE UpdateShipCrewRole
    @IDShipCrewRole int,
    @ShipID int, @CrewRoleID int
AS
BEGIN
    UPDATE ShipCrewRole
    SET ShipID = @ShipID, CrewRoleID = @CrewRoleID
    WHERE IDShipCrewRole = @IDShipCrewRole;
END;

GO

CREATE PROCEDURE DeleteShipCrewRole
    @IDShipCrewRole int
AS
BEGIN
    DELETE FROM ShipCrewRole WHERE IDShipCrewRole = @IDShipCrewRole;
END;

GO
--CurrentLocation
--Table Creation SQL:
CREATE TABLE CurrentLocation (
    IDCurrentLocation int PRIMARY KEY IDENTITY(1,1),
    ShipID int FOREIGN KEY REFERENCES Ship(IDShip),
    Latitude float,
    Longitude float
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertCurrentLocation
    @ShipID int, @Latitude float, @Longitude float
AS
BEGIN
    INSERT INTO CurrentLocation (ShipID, Latitude, Longitude)
    VALUES (@ShipID, @Latitude, @Longitude);
END;

GO

CREATE PROCEDURE SelectCurrentLocation
AS
BEGIN
    SELECT * FROM CurrentLocation;
END;

GO

CREATE PROCEDURE SelectSingleCurrentLocation
    @ShipID int
AS
BEGIN
    SELECT * FROM CurrentLocation
    WHERE ShipID = @ShipID;
END;

GO

CREATE PROCEDURE UpdateCurrentLocation
    @IDCurrentLocation int,
    @ShipID int, @Latitude float, @Longitude float
AS
BEGIN
    UPDATE CurrentLocation
    SET ShipID = @ShipID, Latitude = @Latitude, Longitude = @Longitude
    WHERE IDCurrentLocation = @IDCurrentLocation;
END;

GO

CREATE PROCEDURE DeleteCurrentLocation
    @IDCurrentLocation int
AS
BEGIN
    DELETE FROM CurrentLocation WHERE IDCurrentLocation = @IDCurrentLocation;
END;

GO
--Booking
--Table Creation SQL:
CREATE TABLE Booking (
    IDBooking int PRIMARY KEY IDENTITY(1,1),
    UserID int FOREIGN KEY REFERENCES RegisteredUser(IDUser),
    ShipID int FOREIGN KEY REFERENCES Ship(IDShip)
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertBooking
    @UserID int, @ShipID int
AS
BEGIN
    INSERT INTO Booking (UserID, ShipID)
    VALUES (@UserID, @ShipID);
END;

GO

CREATE PROCEDURE SelectBooking
AS
BEGIN
    SELECT * FROM Booking;
END;

GO

CREATE PROCEDURE SelectUsersBookings
    @UserID int
AS
BEGIN
    SELECT * FROM Booking
    WHERE UserID = @UserID;
END;

GO

CREATE PROCEDURE UpdateBooking
    @IDBooking int,
    @UserID int, @ShipID int
AS
BEGIN
    UPDATE Booking
    SET UserID = @UserID, ShipID = @ShipID
    WHERE IDBooking = @IDBooking;
END;

GO

CREATE PROCEDURE DeleteBooking
    @IDBooking int
AS
BEGIN
    DELETE FROM Booking WHERE IDBooking = @IDBooking;
END;

GO
--Message
--Table Creation SQL:
CREATE TABLE Message (
    IDMessage int PRIMARY KEY IDENTITY(1,1),
    SenderID int FOREIGN KEY REFERENCES RegisteredUser(IDUser),
    RecipientID int FOREIGN KEY REFERENCES RegisteredUser(IDUser),
    Body nvarchar(200),
    IsDelivered bit
);
GO

--CRUD Operations SQL:

CREATE PROCEDURE InsertMessage
    @SenderID int, @RecipientID int, @Body nvarchar(200), @IsDelivered bit
AS
BEGIN
    INSERT INTO Message (SenderID, RecipientID, Body, IsDelivered)
    VALUES (@SenderID, @RecipientID, @Body, @IsDelivered);
END;

GO

CREATE PROCEDURE SelectMessage
AS
BEGIN
    SELECT * FROM Message;
END;

GO

CREATE PROCEDURE SelectUndeliveredMessages
    @RecipientID int
AS
BEGIN
    SELECT * FROM Message
    WHERE RecipientID = @RecipientID AND IsDelivered = 0;
END;

GO

CREATE PROCEDURE MarkMessagesAsDelivered
    @IDMessage int
AS
BEGIN
    UPDATE Message
    SET IsDelivered = 1
    WHERE IDMessage = @IDMessage;
END;

GO

CREATE PROCEDURE UpdateMessage
    @IDMessage int,
    @SenderID int, @RecipientID int, @Body nvarchar(200), @IsDelivered bit
AS
BEGIN
    UPDATE Message
    SET SenderID = @SenderID, RecipientID = @RecipientID, Body = @Body, IsDelivered = @IsDelivered
    WHERE IDMessage = @IDMessage;
END;

GO

CREATE PROCEDURE DeleteMessage
    @IDMessage int
AS
BEGIN
    DELETE FROM Message WHERE IDMessage = @IDMessage;
END;

GO
