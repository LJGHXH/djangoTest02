import requests, pprint

# 模拟登陆
payloadLogin = {
    'username': 'lanjack',
    'password': 'ASD456ZXC123lj',
}
responseLogin = requests.post('http://127.0.0.1:8000/api/mngr/signin', data=payloadLogin)
pprint.pprint(responseLogin.json())

# 模拟查客户
payloadListCustomer = {
    'action': 'list_customer'
}
responseListCustomer = requests.get('http://127.0.0.1:8000/api/mngr/customers', params=payloadListCustomer)
pprint.pprint(responseListCustomer.json())

# 模拟添加客户
payloadAddCustomer = {
    'action':'add_customer',
    'data':{
        'name':'荒坂工业集团',
        'phonenumber':'114514',
        'address':'夜之城荒坂工业集团大厦'
    }
}
responseAddCustomer = requests.post('http://127.0.0.1:8000/api/mngr/customers', json=payloadAddCustomer)
pprint.pprint(responseAddCustomer.json())

# 模拟修改客户信息
payloadModifyCustomer = {
    "action":"modify_customer",
    "id": 6,
    "newdata":{
        "name":"荒坂工业集团",
        "phonenumber":"13345678888",
        "address":"日本东京荒坂集团工业园"
    }
}
responseModifyCustomer = requests.post('http://127.0.0.1:8000/api/mngr/customers', json=payloadModifyCustomer)
pprint.pprint(responseModifyCustomer)

payloadDelCustomer = {
    "action":"del_customer",
    "id": 7
}
responseDelCustomer =requests.post('http://127.0.0.1:8000/api/mngr/customers', json=payloadDelCustomer)
pprint.pprint(responseDelCustomer)