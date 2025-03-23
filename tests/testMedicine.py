import requests, pprint

# 模拟登陆
payloadLogin = {
    'username': 'lanjack',
    'password': 'ASD456ZXC123lj',
}
responseLogin = requests.post('http://127.0.0.1:8000/api/mngr/signin', data=payloadLogin)
pprint.pprint(responseLogin.json())

# 模拟查药品
payload_list_medicine = {
    'action': 'list_medicine'
}
responseListCustomer = requests.get('http://127.0.0.1:8000/api/mngr/medicines', params=payload_list_medicine)
pprint.pprint(responseListCustomer.json())

# 模拟添加药品
payload_add_medicine = {
    "action":"add_medicine",
    "data":{
        "desc": "阿司匹林肠溶缓释片",
        "name": "阿司匹林",
        "sn": "15645646"
    }
}
responseAddCustomer = requests.post('http://127.0.0.1:8000/api/mngr/medicines', json=payload_add_medicine)
pprint.pprint(responseAddCustomer.json())

# 模拟修改药品信息
payload_modify_medicine = {
    "action":"modify_medicine",
    "id": 1,
    "newdata":{
        "name": "青霉素2",
        "desc": "青霉素 国字号22",
        "sn": "0998778838388"
    }
}
responseModifyCustomer = requests.post('http://127.0.0.1:8000/api/mngr/medicines', json=payload_modify_medicine)
pprint.pprint(responseModifyCustomer)

# 删除药品
payload_del_medicine = {
    "action":"del_medicine",
    "id": 6666
}
responseDelCustomer =requests.post('http://127.0.0.1:8000/api/mngr/medicines', json=payload_del_medicine)
pprint.pprint(responseDelCustomer)