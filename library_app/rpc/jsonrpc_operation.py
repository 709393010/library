
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
    #创建图书记录
    create_data = [
        {'name' : 'Book 5','date_published' : '2020-11-11'},
        {'name' : 'Book 6','date_published' : '2020-11-12'},
        {'name' : 'Book 7','date_published' : '2020-11-13'}
    ]
    payload = get_json_payload("object","execute_kw",db_name,user_id,password,'library.book','create',[create_data])
    res = requests.post(json_endpoint,data = payload, headers = headers).json()
    print("Books created:",res)
    book_ids = res['result']

    #写入已有图书记录
    book_to_write = book_ids[1]
    write_data = {'name' : 'Book test'}
    payload = get_json_payload("object","execute_kw",db_name,user_id,password,'library.book','write',[[90],write_data])
    res = requests.post(json_endpoint, data=payload,headers=headers).json()
    print("Book written:",res)

    # #在已有图书记录中进行删除
    book_to_unlink = book_ids[2:]
    payload = get_json_payload("object","execute_kw",db_name,user_id,password,'library.book','unlink',[[91]])
    res = requests.post(json_endpoint,data=payload,headers=headers).json()
    print("Books deleted:",res)
    
else:
    print("Failed wrong credentials")


