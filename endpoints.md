# Prijedlog API-ja (klijent)
Ovo je popis funkcija API-ja s primjerima koji sluzi kao referenca.
## /register
Registracija korisnika, API na zahtjev trazi korisnika u bazi i ako ne postoji kreira korisnika u bazi i vraca izvjestaj o uspjehu.
### Request
```js
{
    "email": "neki@mail.com"
    "username": "riba",
    "password": "nekalozinka123",
    "iznajmljivac": false
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false,
    "reason": "username_taken"
}
```
Moguci razlozi: `username_taken`, `email_taken`.


## /login
Prijava korisnika, API na zahtjev trazi korisnika u bazi i ako postoji i lozinka odgovara, vraca token koji ce se koristiti u daljnjoj komunikaciji.
### Request
```js
{
    "username": "riba",
    "password": "nekalozinka123"
}
```

### Response (success)
```js
{
    "success": true,
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response (failure)
```js
{
    "success": false
}
```


## /logout
Odjava korisnika, API brise trenutno aktivan token.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false
}
```


## /ships
Dohvat svih linija, moguce dodati `/<id>` na kraj za dohvat jedne linije.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response
```js
[
    {
        "id": 0,
        "owner": "ribetina",
        "type": "catamaran",
        "length": 30,
        "berths": 3,
        "bathrooms": 3,
        "equipment": [
            "A/C", "inverter", "generator", "water purifier"
        ],
        "crew": [
            "skipper", "host"
        ],
        "route": [
            "Split", "Brac", "Hvar", "Vis", "Split"
        ]
    },
    {
        "id": 1,
        "owner": "ribetina",
        "type": "monohull",
        "length": 20,
        "berths": 2,
        "bathrooms": 1,
        "equipment": [],
        "crew": [],
        "route": [
            "Zadar", "Dugi Otok", "Kornati", "Zut", "Zadar"
        ]
    }
]
```

### Response (za npr. `/ships/0`)
```js
{
    "id": 0,
    "owner": "ribetina",
    "type": "catamaran",
    "length": 30,
    "berths": 3,
    "bathrooms": 3,
    "equipment": [
        "A/C", "inverter", "generator", "water purifier"
    ],
    "crew": [
        "skipper", "host"
    ],
    "route": [
        "Split", "Brac", "Hvar", "Vis", "Split"
    ]
}
```

## /shipLocation/\<id\>
Dohvaca trenutnu lokaciju broda.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response (success)
```js
{
    "success": true
    "latitude": 45.516,
    "longitude": -122.636
}
```

### Response (failure)
```js
{
    "success": false
}
```


## /bookShip/\<id\>
Zahtjev za rezervacijom broda.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false
}
```


## /bookedShips
Dohvat svih rezerviranih linija za trenutnog korisnika
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response
```js
[
    {
        "id": 0,
        "type": "catamaran",
        "length": 30,
        "berths": 3,
        "bathrooms": 3,
        "equipment": [
            "A/C", "inverter", "generator", "water purifier"
        ],
        "crew": [
            "skipper", "host"
        ],
        "route": [
            "Split", "Brac", "Hvar", "Vis", "Split"
        ]
    },
    {
        "id": 1,
        "type": "monohull",
        "length": 20,
        "berths": 2,
        "bathrooms": 1,
        "equipment": [],
        "crew": [],
        "route": [
            "Zadar", "Dugi Otok", "Kornati", "Zut", "Zadar"
        ]
    }
]
```

### Response (empty)
```js
[]
```


## /receiveMessages
Dohvat svih novih poruka poslanih korisniku.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response
```js
[
    {
        "from": "ribetina",
        "sent": "2012-04-23T18:25:43.511Z",
        "body": "Riba ribi grize rep"
    },
    {
        "from": "ribetina",
        "sent": "2012-04-23T18:26:43.511Z",
        "body": "Oces ribicu?"
    }
]
```

### Response (empty)
```js
[]
```


## /sendMessage
Zahtjev za slanjem poruke nekom korisniku.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb",
    "to": "ribetina",
    "body": "hocuuuuu :)"
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false
}
```


# Prijedlog API-ja (iznajmljivac)
Iznajmljivaci imaju sve iste pozive kao i klijent, te jos ove dodatne.

## /addShip
Dodaje liniju u dostupne linije.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
    "ship": {
        "type": "catamaran",
        "length": 30,
        "berths": 3,
        "bathrooms": 3,
        "equipment": [
            "A/C", "inverter", "generator", "water purifier"
        ],
        "crew": [
            "skipper", "host"
        ],
        "route": [
            "Split", "Brac", "Hvar", "Vis", "Split"
        ]
    }
}
```

### Response (success)
```js
{
    "success": true,
    "id": 0
}
```

### Response (failure)
```js
{
    "success": false
}
```

## /updateShip
Mijenja podatke linije.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
    "ship": {
        "id": 0
        "type": "catamaran",
        "length": 30,
        "berths": 3,
        "bathrooms": 3,
        "equipment": [
            "A/C", "inverter", "generator", "water purifier"
        ],
        "crew": [
            "skipper", "host"
        ],
        "route": [
            "Split", "Brac", "Hvar", "Vis", "Split"
        ]
    }
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false
}
```


## /deleteShip/\<id\>
Brise liniju.
### Request
```js
{
    "token": "03bb02c4-a3f1-478f-8ea9-fc376539f8fb"
}
```

### Response (success)
```js
{
    "success": true
}
```

### Response (failure)
```js
{
    "success": false
}
```