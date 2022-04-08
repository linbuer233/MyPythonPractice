'''
实现连校园网
1.打开wifi
2.登陆校园网
'''

import os
import time

import requests

os.system('netsh wlan connect name=i-NUIST')
time.sleep(2)
print('连接中')

data = {
    "reauth": 'false',
    "username": "your_phone_number",  #
    "balance": "0.00",
    "duration": "0",
    "outport": "中国移动",  #
    "totaltimespan": "0",
    "usripadd": "10.0.204.91"
}

data1 = {
    "username": "your_phone_number",  #
    "password": "123789",  # 密码
    "channel": "2",
    "ifautologin": "0",  #
    "pagesign": "secondauth",
    "usripadd": "10.0.204.92"
}
r = requests.post('http://10.255.255.34/authentication/login', data=data)
print('连接成功')
