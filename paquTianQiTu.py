'''
实现在中央气象台批量下载天气图，并分类存放在各自文件夹中
'''
import os
import time

import requests
from selenium import webdriver
## 导入selenium的浏览器驱动接口
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

levels = ['地面', '925hPa', '850hPa', '700hPa', '500hPa', '200hPa', '100hPa']
bigmonth = ['01', '03', '04', '05', '07', '08', '10', '12']
area = ['中国', '亚欧']

###################################################打开驱动浏览器软件，并打开网页#############################################
'''已弃用'''
# chromedriver = 'D:\\chromedriver_win32\\' + 'chromedriver.exe'  ########前面改成自己浏览器驱动器的路径
# #chromedriver的文件位置
# driver = webdriver.Chrome(ChromeDriverManager().install())
'''已弃用'''
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# #加载浏览器驱动
driver.get('http://www.nmc.cn/publish/observations/china/dm/weatherchart-h000.html')
# #打开天气图页面
driver.maximize_window()
time.sleep(2)  # 休息
#######################################################################################################################
for area_i in area:
    ########################################选择模块####################################################################
    ########### 模拟鼠标选择高度层
    button1 = driver.find_element(by=By.LINK_TEXT, value=area_i)
    # 通过link文字精确定位元素
    action = ActionChains(driver).move_to_element(button1)
    # 鼠标悬停在一个元素上
    action.click(button1).perform()
    # 鼠标单击
    time.sleep(2)
    # 注意加等待时间，避免因速度太快而失败
    ####################################################################################################################
    for levels_i in levels:
        ########################################选择模块##################################################################
        ########### 模拟鼠标选择高度层
        button1 = driver.find_element(by=By.LINK_TEXT, value=levels_i)
        # 通过link文字精确定位元素
        action = ActionChains(driver).move_to_element(button1)
        # 鼠标悬停在一个元素上
        action.click(button1).perform()
        # 鼠标单击
        time.sleep(2)
        # 注意加等待时间，避免因速度太快而失败
        ####################################################################################################################

        list = driver.find_elements(by=By.XPATH, value='//*[@id="mCSB_1_container"]/div')  ##存放天气图各个时刻一起的Xpath路径
        for path in list:  ##依次读取下载存放天气图
            img_url = path.find_element(by=By.XPATH, value='.').get_attribute('data-img')  # 在网页源码的同一级下 用 .
            img_name = path.find_element(by=By.XPATH, value='.').get_attribute('data-img')

            img_name = img_name[-37:-25]  #### 截取到日期方便后面命名存放
            img_name_year = img_name[:4]
            img_name_month = img_name[4:6]
            img_name_day = img_name[6:8]
            img_name_hour = str(int(img_name[8:12]) + 10800)  ###转换成北京时间，并且为了小时分钟显示0000这样的格式，加了10800，后面再截取

            ####对日期的处理，有些加了八小时变成北京时间之后，日期会发生改变，下面就是对日期在闰年、非闰年，大小月等情况时的处理
            if int(img_name_hour) > 12400:
                img_name_day = str(int(img_name_day) + 101)
                img_name_day = img_name_day[1:3]
                img_name_hour = str(int(img_name_hour) - 2400)
                img_name_hour = img_name_hour[1:5]
                if int(img_name_year) % 4 == 0 and int(img_name_year) % 100 != 0:  ####闰年的判定
                    if img_name_month == '02':
                        if int(img_name_day) > 29:
                            img_name_day = '01'
                    if img_name_month in bigmonth:
                        if int(img_name_day) > 31:
                            if img_name_month == '12':
                                img_name_month = '01'
                            else:
                                img_name_month = str(int(img_name_month) + 101)[1:]
                            img_name_day = '01'
                    else:
                        if int(img_name_day) > 30:
                            img_name_month = str(int(img_name_month) + 101)[1:]
                            img_name_day = '01'
                else:
                    if img_name_month == '02':
                        if int(img_name_day) > 28:
                            img_name_day = '01'
                    if img_name_month in bigmonth:
                        if int(img_name_day) > 31:
                            if img_name_month == '12':
                                img_name_month = '01'
                            else:
                                img_name_month = str(int(img_name_month) + 101)[1:]
                            img_name_day = '01'
                    else:
                        if int(img_name_day) > 30:
                            img_name_month = str(int(img_name_month) + 101)[1:]
                            img_name_day = '01'
            else:
                img_name_hour = img_name_hour[1:5]

            page = requests.get(img_url)  #### 在链接中找到图片
            img = page.content  #### 存取二进制的图片

            img_name_uppath = 'd:\\picture\\' + area_i + '\\' + levels_i + '\\' + img_name_year + '\\' + img_name_month  ###前面的 'd:\\picture\\'可以改成自己存放图片的路径
            if not os.path.exists(img_name_uppath):  ####创建多级目录，在不存在这个目录的情况下
                os.makedirs(img_name_uppath)

            img_name_path = img_name_uppath + '\\' + img_name_year + '_' + img_name_month + '_' + img_name_day + '_' + img_name_hour + '.jpg'
            with open(img_name_path, mode='wb') as f:
                f.write(img)
