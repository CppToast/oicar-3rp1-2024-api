import requests
import json

url = 'http://localhost:5000/'

def make_request(suburl, data):
    global url
    newurl = url + suburl
    return requests.post(newurl, json=data)


# suburl = 'register'
# data = {
#     "email": "b@b.b",
#     "username": "bbb",
#     "password": "123",
#     "renter": False
# }

# suburl = 'login'
# data = {
#     "username": "bbb",
#     "password": "123"
# }

suburl = 'logout'
data = {
    "token":"16A6C8EE-0630-4EEE-B3FD-C7F039891EDB"
}

req = make_request(suburl, data)

print("Status code:", req.status_code)
print("Data:", req.text)