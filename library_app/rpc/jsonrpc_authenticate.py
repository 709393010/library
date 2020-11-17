import json
import random
import requests

server_url = 'http://localhost:8888'
db_name = 'odoo12'
username = 'root'
password = '123456'

json_endpoint = "%s/jsonrpc" % server_url
headers = {"Content-Type" : "application/json"}

def get_json_payload(service,method,*args):
    return json.dumps({
        "jsonrpc" : "2.0",
        "method" : "call",
        "params" : {
            "service" : service,
            "method" : method,
            "args" : args
        },
        "id" : random.randint(0,10000000),
    }) 

payload = get_json_payload("common","login",db_name, username, password)
response = requests.post(json_endpoint, data=payload, headers=headers)
user_id = response.json()['result']

# payload = get_json_payload("common","version")
# response = requests.post(json_endpoint, data = payload, headers = headers)
# print(response.json())

if user_id:
    print("Success User id is",user_id)
else:
    print("Failed:wrong credentials")
