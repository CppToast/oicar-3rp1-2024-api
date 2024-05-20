from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    username: str
    passwordhash: str
    renter: bool

@dataclass
class Token:
    id: int
    user_id: int
    guid: str

@dataclass
class Ship:
    id: int
    owner: str
    type: str
    length: float
    berths: int
    bathrooms: int
    equipment: list
    crew: list
    route: list

@dataclass
class ShipLocation:
    latitude: float
    longitude: float

@dataclass
class Message:
    sender: str
    recipient: str
    sent: str
    body: str


