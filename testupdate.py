import requests
import json
from flask import request

# new_person = {
    # }
new_person = {
	"photo": 'C:/Users/brett/OneDrive/Documents/IDS594CA/business_cards/Canon/007.jpg'
}
headers = {
	'Content-type': 'application/json'
	}

# getResp = requests.get('http://127.0.0.1:5000/api/connectme/new_user')
# print(getResp.json()["request data"].keys())

resp = requests.post('http://127.0.0.1:5000/api/connectme/new_user', json=new_person, headers=headers)
print(resp.text)
print(resp.json()["output"]["name"])

# getResp = requests.get('http://127.0.0.1:5000/api/connectme/new_user')
# print(getResp.json())