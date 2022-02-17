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
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

bigmonth = ['01', '03', '04', '05', '07', '08', '10', '12']
levels = ['/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[1]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[2]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[3]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[4]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[5]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[6]/a',
          '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/ul/li[7]/a']
levels1 = ['地面', '925hPa', '850hPa', '700hPa', '500hPa', '200hPa', '100hPa']
area = ['/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul/li[1]/a',
        '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul/li[2]/a']
area1=['中国','亚欧']
###################################################打开驱动浏览器软件，并打开网页#############################################
try:
    with open('PaquTianqiTu_config.txt', 'r') as a:
        f = open('PaquTianqiTu_config.txt', 'r')
        path = f.readline()
        f.close()
        f = open(path, 'r')
        webnum = f.readline()[:-1]
        picturepath = f.readline()
except:
    print("第一次使用吗？Y/n")
    while True:
        a = input()
        if a == 'n' or a == 'N' or a == 'no' or a == 'No':
            print('找不到程序配置文件，需遵守下面的操作重新配置。')
            break
        if a == 'Y' or a == 'y' or a == 'yes' or a == 'Yes':
            print('请遵守下面的操作开始配置。')
            break
        print('输入错误，请重新输入。')
    print('①请输入配置文件所需在的路径(格式为: d:\\path\\path1)。')
    print('ps:尽量不要选择C盘下的路径，除非确保有权限在C盘写入文件。')
    while True:
        inputpath = input()
        configpath = inputpath + '\\' + 'PaquTianqiTu_config.txt'
        if inputpath[1:3] != ':\\':
            print("输入错误，注意格式为: d:\\path\\path1")
            continue
        try:
            if not os.path.exists(inputpath):
                os.makedirs(inputpath)
            f = open(configpath, 'w')
            f.close()
            break
        except:
            print("输入错误，注意格式为: d:\\path\\path1")
    print('\n')
    print('②输入你所使用的浏览器，输入序号即可')
    print('Edge(微软自带)\t1')
    print('FireFox(火狐)\t2')
    print('Chrome(谷歌)\t3')
    while True:
        webnumber = input()
        if webnumber == '1' or webnumber == '2' or webnumber == '3':
            break
        print("输入错误，请输入阿拉伯数字")
    print('\n')
    print('③输入图片的存放路径')
    print('注意格式与上面的路径一样')
    while True:
        picturepath = input()
        if picturepath[1:3] != ':\\':
            print('输入错误，请重新输入。')
            continue
        try:
            if not os.path.exists(picturepath):
                os.makedirs(picturepath)
            f = open(picturepath + '\\' + 'hh.txt', 'w')
            f.close()
            os.remove(picturepath + '\\' + 'hh.txt')
            break
        except:
            print('输入错误，请重新输入。')
    print('\n')
    f = open("PaquTianqiTu_config.txt", 'w')
    f.write(configpath)
    f.close()
    f = open(configpath, 'w')
    f.write(webnumber)
    f.write('\n')
    f.write(picturepath)
    f.close()
    print('配置结束，谢谢 ^_^ ')
if webnum == '1':
    # Edge
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
if webnum == '2':
    # FireFox
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
if webnum == '3':
    # Chrome
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
# #加载浏览器驱动
driver.get('http://www.nmc.cn/publish/observations/china/dm/weatherchart-h000.htm')
# #打开天气图页面
driver.maximize_window()
time.sleep(2)  # 休息
#######################################################################################################################
for area_i in area:
    ########################################选择模块####################################################################
    ########### 模拟鼠标选择高度层
    button1 = driver.find_element(by=By.XPATH, value=area_i)
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
        button1 = driver.find_element(by=By.XPATH, value=levels_i)
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
            '''
            你存放文件的路径
            '''
            img_name_uppath = picturepath + '\\' + area1[area.index(area_i)] + '\\' + levels1[levels.index(levels_i)] + '\\' + img_name_year + '\\' + img_name_month  ###前面的 'd:\\picture\\'可以改成自己存放图片的路径
            if not os.path.exists(img_name_uppath):  ####创建多级目录，在不存在这个目录的情况下
                os.makedirs(img_name_uppath)

            img_name_path = img_name_uppath + '\\' + img_name_year + '_' + img_name_month + '_' + img_name_day + '_' + img_name_hour + '.jpg'
            with open(img_name_path, mode='wb') as f:
                f.write(img)
