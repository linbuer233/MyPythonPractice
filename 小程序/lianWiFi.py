'''
实现连校园网
1.打开wifi
2.登陆校园网
'''

import os
import time

os.system('netsh wlan connect name=i-NUIST')
time.sleep(2)
print('连接中')
from selenium import webdriver
## 导入selenium的浏览器驱动接口
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 链接校园网
driver.get('https://www.baidu.com/')
time.sleep(2)
# /html/body/div[1]/div[2]/div[5]/div[1]/div/form/span[1]/input//*[@id="kw"]
# /html/body/div[1]/div[1]/div[5]/div/div/form/span[1]/input
driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[5]/div[1]/div/form/span[1]/input").get_attribute("id").send_keys("hh")
# driver.find_element(by=By.XPATH,value='/html/body/div/div/div[2]/div[1]/form/div/div[1]/div/div/span/span/input').send_keys("18705160127")
time.sleep(2)
# input.send_keys("18705160127")
#
# data = {
#     "username": "18705160127",  #
#     "password": "123789",  # 密码
#     "R1": "0",
#     "R3": "1",
#     "R6": "0",
#     "pare": "00",
#     "OMKKey": "123456"
# }
#
# header = {
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
#     "Connection": "keep-alive",
#     "Content-Length": "128",
#     "Content-Type": "application/json;charset=UTF-8",
#     "Host": "10.255.255.34",
#     "Origin": "http://10.255.255.34",
#     "Referer": "http://10.255.255.34/authentication/login",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"
# }
#
# r = requests.post('http://10.255.255.34/authentication', data=data, headers=header).status_code
# print("回应代码{}".format(r))
# print('连接成功')
