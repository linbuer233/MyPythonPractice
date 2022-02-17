import requests
from bs4 import BeautifulSoup
from lxml import etree

url = 'http://www.weather.com.cn/weather1d/101300703.shtml'
r = requests.get(url=url)
r.encoding = r.apparent_encoding
a = r.text
b=etree.HTML(a)
s=b.xpath("""//*[@id="7d"]/ul/li[1]/p[2]/i/text()""")
print(s)
# soup = BeautifulSoup(a, features='lxml')
# # a1=soup.find('body > div.contoday.clearfix > div.left.fl > divleft-div > div#today > div.t > div > div.tem')
# a1 = soup.select('#today > div.t')
# a2=soup.select('#today > div.t > div')
# print(a1)
# print(a2)