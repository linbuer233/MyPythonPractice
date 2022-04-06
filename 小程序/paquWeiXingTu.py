'''
实现在中央气象台批量下载卫星云图，并存放在各自文件夹中
'''
import os
import time

import requests
from selenium import webdriver
## 导入selenium的浏览器驱动接口
from selenium.webdriver.common.action_chains import ActionChains

lei = ['FY4A红外', 'FY4A可见光', 'FY4A水汽']
bigmonth = ['01', '03', '04', '05', '07', '08', '10', '12']

#######################################################################################################################
chrome_driver = 'D:\\chromedriver_win32\\' + 'chromedriver.exe'
# #chromedriver的文件位置
driver = webdriver.Chrome(executable_path=chrome_driver)
# #加载浏览器驱动
driver.get('http://www.nmc.cn/publish/satellite/FY4A-true-color.htm')
# #打开天气图页面
driver.maximize_window()
time.sleep(2)  # 休息
#######################################################################################################################
for lei_i in lei:
    ########################################选择模块######################################################################
    ########### 模拟鼠标选择雷达类型
    button1 = driver.find_element_by_link_text(lei_i)
    # 通过link文字精确定位元素
    action = ActionChains(driver).move_to_element(button1)
    # 鼠标悬停在一个元素上
    action.click(button1).perform()
    # 鼠标单击
    time.sleep(2)
    # 注意加等待时间，避免因速度太快而失败
    ####################################################################################################################
    list = driver.find_elements_by_xpath('// *[ @ id = "mCSB_1_container"] / div')
    for path in list:
        img_url = path.find_element_by_xpath('.').get_attribute('data-img')  # 在网页源码的同一级下 用 .
        img_name = path.find_element_by_xpath('.').get_attribute('data-img')

        img_name = img_name[-37:-25]  #### 截取到日期方便后面命名存放
        img_name_year = img_name[:4]
        img_name_month = img_name[4:6]
        img_name_day = img_name[6:8]
        img_name_hour = str(int(img_name[8:12]) + 10800)  ###转换成北京时间并且为了小时分钟显示0000这样的格式，加了10800，后面再截取

        #######对日期的处理，有些加了八小时变成北京时间之后，日期会发生改变，下面就是对日期在闰年、非闰年，大小月等情况时的处理
        if int(img_name_hour) > 12400:
            img_name_day = str(int(img_name_day) + 101)
            img_name_day = img_name_day[1:3]
            img_name_hour = str(int(img_name_hour) - 2400)
            img_name_hour = img_name_hour[1:5]
            if int(img_name_year) % 4 == 0 and int(img_name_year) % 100 != 0:
                if img_name_month == '02':
                    if int(img_name_day) > 29:
                        img_name_day = '01'
                if img_name_month in bigmonth:
                    if int(img_name_day) > 31:
                        img_name_month = str(int(img_name_month) + 1)
                        img_name_day = '01'
                else:
                    if int(img_name_day) > 30:
                        img_name_month = str(int(img_name_month) + 1)
                        img_name_day = '01'
            else:
                if img_name_month == '02':
                    if int(img_name_day) > 28:
                        img_name_day = '01'
                if img_name_month in bigmonth:
                    if int(img_name_day) > 31:
                        img_name_month = str(int(img_name_month) + 1)
                        img_name_day = '01'
                else:
                    if int(img_name_day) > 30:
                        img_name_month = str(int(img_name_month) + 1)
                        img_name_day = '01'
        else:
            img_name_hour = img_name_hour[1:5]

        page = requests.get(img_url)  #### 在链接中找到图片
        img = page.content  #### 存取二进制的图片

        img_name_uppath = 'd:\\picture\\雷达\\' + lei_i + '\\' + img_name_year + '\\' + img_name_month + '\\' + img_name_day
        if not os.path.exists(img_name_uppath):  ####创建多级目录，在不存在这个目录的情况下
            os.makedirs(img_name_uppath)

        img_name_path = img_name_uppath + '\\' + img_name_year + '_' + img_name_month + '_' + img_name_day + '_' + img_name_hour + '.jpg'
        with open(img_name_path, mode='wb') as f:
            f.write(img)
