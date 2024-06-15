import os
import datetime
from io import BytesIO

import PIL.Image
import requests
from bs4 import BeautifulSoup
import wget
import PIL

# 爬取雷达图
url = "http://www.nmc.cn/publish/radar/huanan.html"
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
listyuan = soup.find_all("div", attrs={"data-fffmm": "000"})
imglist = []
for i in listyuan:
    imglist.append(i.get("data-img"))

# 爬取雷达图
path = "./radar/" + str(datetime.datetime.now())[:10] + "/"
if not os.path.exists(path):
    os.makedirs(path)
    print("创建文件夹成功")

print("开始下载雷达图")
for i in imglist:
    # 转换成北京时间
    filename = wget.filename_from_url(i)[-21:-9]
    filename = datetime.datetime.strptime(filename, "%Y%m%d%H%M") + datetime.timedelta(
        hours=8
    )
    filename = filename.strftime("%Y%m%d%H%M") + ".png"

    image = PIL.Image.open(BytesIO(requests.get(i).content))
    upx = 400
    upy = 20
    imgw = 256
    image = image.crop((upx, upy, upx + imgw, upy + imgw))
    image.save(os.path.join(path, filename))
