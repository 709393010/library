
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

if user_id:
    search_domain = ['|',['name','ilike','三'],['name','ilike','光']]
    payload = get_json_payload("object","execute_kw",db_name,user_id,password,'library.book','search',[search_domain],{'limit':5})
    res = requests.post(json_endpoint,data=payload,headers=headers).json()
    print('Search Result:',res)

    payload = get_json_payload("object","execute_kw",db_name,user_id,password,'library.book','read',[res['result'],['name','date_published']])
    res = requests.post(json_endpoint,data=payload, headers = headers).json()
    print('Books data:',res)
else:
    print("Failed:wrong credentials")
