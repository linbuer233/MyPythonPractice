import os
from math import *

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import metpy.calc as mpcalc
import metpy.constants as constants
import numpy as np  # 调用 numpy
import pandas as pd
import xarray as xr
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from metpy.units import units

plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
plt.rcParams['axes.unicode_minus'] = False  ###用来正常显示负号


##时间处理，加个八小时
def shijianchuli(img_name):
    bigmonth = ['01', '03', '04', '05', '07', '08', '10', '12']
    img_name_year = img_name[:4]
    img_name_month = img_name[4:6]
    img_name_day = img_name[6:8]
    img_name_hour = str(int(img_name[8:10]) + 108)  ###转换成北京时间，并且为了小时显示 00 这样的格式，加了 108，后面再截取

    ####对日期的处理，有些加了八小时变成北京时间之后，日期会发生改变，下面就是对日期在闰年、非闰年，大小月等情况时的处理
    if int(img_name_hour) > 124:
        img_name_day = str(int(img_name_day) + 101)
        img_name_day = img_name_day[1:3]
        img_name_hour = str(int(img_name_hour) - 24)
        img_name_hour = img_name_hour[1:3]
        if int(img_name_year) % 4 == 0 and int(img_name_year) % 100 != 0:  ####闰年的判定
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
        img_name_hour = img_name_hour[1:3]
    daytime = img_name_year + '_' + img_name_month + '_' + img_name_day + '_' + img_name_hour
    return daytime


##地图创建函数
def createmap():
    ###################################地图设置##########################
    fig = plt.figure(figsize=(9, 6), dpi=150)  # 画布大小
    ax = fig.subplots(1, 1,
                      subplot_kw={'projection': ccrs.LambertConformal(central_longitude=105, central_latitude=30)})
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_geometries(Reader('D:\\maplist\\China_province\\bou2_4l.shp').geometries(), ccrs.PlateCarree(),
                      facecolor='none', edgecolor='gray', linewidth=0.8)  ###添加省界
    ax.add_geometries(Reader('D:\\maplist\\zhengzhou\\郑州市.shp').geometries(), ccrs.PlateCarree(),
                      facecolor='none', edgecolor='r', linewidth=0.8)  ###添加郑州市界
    Lam = ax.gridlines(draw_labels=True, linestyle=':', linewidth=0.3, x_inline=False, y_inline=False, color='k')
    Lam.top_labels = True  ##打开上面的经纬度标签
    Lam.right_labels = False  ###关闭右边
    Lam.xformatter = LONGITUDE_FORMATTER
    Lam.yformatter = LATITUDE_FORMATTER
    Lam.xlocator = mticker.FixedLocator(np.arange(0, 180, 10))
    Lam.ylocator = mticker.FixedLocator(np.arange(10, 80, 10))
    Lam.xlabel_style = {'size': 7}
    Lam.ylabel_style = {'size': 7}
    ax.set_extent([60, 135, 10, 70], ccrs.PlateCarree())  ## 调整图片大小在画布中

    return ax, fig


all = xr.open_dataset(r'D:\python\tianzhen\shixi3_4\ds_hgt_t_uv.nc')
rh_all = xr.open_dataset(r'D:\python\tianzhen\shixi3_4\ds_rh.nc')
hgt = all['hgt'][:, :, :, :]
Temp = all['t'][:, :, :, :]
rh = rh_all['rh'][:, :, :, :]
lon = all['lon'][:]
lat = all['lat'][:]
time = all['time'][:]
level = rh_all['level'][:]
rh = rh.data
hgt = hgt.data
hgt1 = hgt * 10 * units.gpm
Temp = (Temp.data + 273.16)
Temp1 = Temp * units.K
P = level.data
P1 = level.data * units.hPa

##定义常量
Rd = 287  ##j/(K*kg)
L = 2.5 * 10 ** 6  # J/kg
Cp = 1004  # J/(K*kg)
a = 17.2693882
b = 35.86

weiwen = np.zeros((len(level), len(time), len(lat), len(lon)))
xiangdangweiwen = np.zeros((len(level), len(time), len(lat), len(lon)))
Td = np.zeros((len(level), len(time), len(lat), len(lon)))
q = np.zeros((len(level), len(time), len(lat), len(lon)))
es = np.zeros((len(lat), len(lon)))
e0 = np.zeros((len(lat), len(lon)))
e = np.zeros((len(lat), len(lon)))
Td0 = np.zeros((len(lat), len(lon)))
###计算露点温度，运行时间过长，所以只运行一次，创建 nc 文件后注释掉
'''
for h_i in range(len(level)):
    for time_i in range(len(time)):
        for j in range(len(lat)):
            for i in range(len(lon)):
                es[j, i] = 6.1078 * np.exp((a * (Temp[h_i, time_i, j, i] - 273.16) / (Temp[h_i, time_i, j, i] - b)))
                e[j, i] = rh[h_i, time_i, j, i] * es[j, i] / 100
                Td0[j, i] = Temp[h_i, time_i, j, i]
                while True:
                    e0[j, i] = 6.1078 * np.exp((a * (Td0[j, i] - 273.16)) / (Td0[j, i] - b))
                    if e[j, i] < e0[j, i]:
                        Td0[j, i] = Td0[j, i] - 0.1
                    else:
                        Td[h_i, time_i, j, i] = Td0[j, i]
                        break
ds_Td = xr.Dataset({'Td': (['level', 'time', 'lat', 'lon'], Td)},
                   coords={'lon': (['lon'], lon.data),
                           'lat': (['lat'], lat.data),
                           'time': (['time'], time.data),
                           'level': (['level'], level.data)
                           })
ds_Td.to_netcdf('D:\\python\\tianzhen\\shixi3_4\\ds_Td.nc')
'''
T = xr.open_dataset('D:\\python\\tianzhen\\shixi3_4\\ds_Td.nc')
Td = T['Td'][:, :, :, :]  ### 单位 K
Td = Td.data * units.K
rh_1 = rh / 100  ###metpy 公式需求  0<rh<1

xdtheta = []  ##存放相当位温
'''
##计算位温和相当位温
for h_i in range(len(level)):
    for time_i in range(len(time)):
        for j in range(len(lat)):
            for i in range(len(lon)):
                weiwen[h_i, time_i, j, i] = Temp[h_i, time_i, j, i] * pow(1000 / P[h_i], 0.286)
                xdtheta.append(
                    mpcalc.equivalent_potential_temperature(P1[h_i], Temp1[h_i, time_i, j, i], Td[h_i, time_i, j, i]))
xdtheta_i = 0
for h_i in range(len(level)):
    for time_i in range(len(time)):
        for j in range(len(lat)):
            for i in range(len(lon)):
                xiangdangweiwen[h_i, time_i, j, i] = xdtheta[xdtheta_i].m
                xdtheta_i = xdtheta_i + 1
ds_weiwen = xr.Dataset({'weiwen': (['level', 'time', 'lat', 'lon'], weiwen),
                        'xiangdangweiwen': (['level', 'time', 'lat', 'lon'], xiangdangweiwen)},
                       coords={'lon': (['lon'], lon.data),
                               'lat': (['lat'], lat.data),
                               'time': (['time'], time.data),
                               'level': (['level'], level.data)
                               })
ds_weiwen.to_netcdf('D:\\python\\tianzhen\\shixi3_4\\ds_weiwen.nc')
'''  ##同理
##计算位势稳定度，k 指数
for h_i in range(len(level)):
    for time_i in range(len(time)):
        for j in range(len(lat)):
            for i in range(len(lon)):
                es[j, i] = 6.1078 * np.exp((a * (Temp[h_i, time_i, j, i] - 273.16) / (Temp[h_i, time_i, j, i] - b)))
                e[j, i] = rh[h_i, time_i, j, i] * es[j, i] / 100
                q[h_i, time_i, j, i] = 622 * e[j, i] / (P[h_i] - 0.378 * e[j, i])
g = 9.8
Ec = np.zeros((len(level), len(time), len(lat), len(lon)))
K = np.zeros((len(time), len(lat), len(lon)))
Plist = list(P)
for time_i in range(len(time)):
    K[time_i, :, :] = Temp[Plist.index(850), time_i, :, :] - Temp[Plist.index(500), time_i, :, :] + Td.m[
                                                                                                    Plist.index(850),
                                                                                                    time_i, :, :] - (
                              Temp[Plist.index(700), time_i, :, :] - Td.m[Plist.index(700), time_i, :, :])
    for h_i in range(len(level)):
        Ec[h_i, time_i, :, :] = Cp * Temp[h_i, time_i, :, :] + g * hgt[h_i, time_i, :, :] + L * q[h_i, time_i, :, :]

######################################################绘图模块###########################################################
weiwenall = xr.open_dataset('D:\\python\\tianzhen\\shixi3_4\\ds_weiwen.nc')
weiwen = weiwenall['weiwen'][:, :, :, :]
xiangdangweiwen = weiwenall['xiangdangweiwen'][:, :, :, :]
##新创建一个时间序列，方便给图片命名，nc 文件中的时间序列弄错了
t1 = pd.date_range(start='20210717', periods=24, freq='6H')  ##用于给图片命名
t2 = pd.date_range(start='2021-07-17 08', periods=24, freq='6H')  ##方便画位温，相当位温给时间轴加 8 小时，由于中间有空格，无法用于图片命名
time1 = np.zeros((len(t1)))
for t_i in range(len(t1)):
    a = str(t1[t_i])
    b = a[:4] + a[5:7] + a[8:10] + a[11:13]
    time1[t_i] = str(shijianchuli(b))
##位温
fig = plt.figure(figsize=(9, 6))
ax = fig.subplots(1, 1)
colorbar = ax.contourf(t2, level, weiwen[:, :, 14, 45], cmap='Spectral')
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
##横坐标格式显示
ax.set_xticks(pd.date_range(start='2021-07-17 08', periods=24, freq='6H'))
plt.xticks(rotation=90)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
##纵坐标格式显示
ax.invert_yaxis()
ax.set_yscale('symlog')
##暴力显示
plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300],
           ["1000", "900", "800", "700", "600", "500", "400", "300"])
ax.set_ylabel('hPa')

titlename = '位温时间——高度剖面图'
ax.set_title(titlename)
ax.grid()
plt.tight_layout()  ##让图填充到整个画布
picturepath = 'D:\\python\\tianzhen\\shixi3_4\\ex5picture\\位温时间 - 高度剖面图'
if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
    os.makedirs(picturepath)
picturename = picturepath + '\\' + titlename + '.png'
plt.savefig(picturename)
plt.close()
##相当位温
fig = plt.figure(figsize=(9, 6))
ax = fig.subplots(1, 1)
colorbar = ax.contourf(t2, level, xiangdangweiwen[:, :, 14, 45], cmap='Spectral')
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
##横坐标格式显示
ax.set_xticks(pd.date_range(start='2021-07-17 08', periods=24, freq='6H'))
plt.xticks(rotation=90)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
##纵坐标格式显示
ax.invert_yaxis()
ax.set_yscale('symlog')
##暴力显示
plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300],
           ["1000", "900", "800", "700", "600", "500", "400", "300"])
ax.set_ylabel('hPa')

titlename = '相当位温时间——高度剖面图'
ax.set_title(titlename)
ax.grid()
plt.tight_layout()  ##让图填充到整个画布
picturepath = 'D:\\python\\tianzhen\\shixi3_4\\ex5picture\\相当位温时间 - 高度剖面图'
if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
    os.makedirs(picturepath)
picturename = picturepath + '\\' + titlename + '.png'
plt.savefig(picturename)
plt.close()

# K 指数
for t_i in range(len(time1)):
    ax, fig = createmap()
    ###按照课本出现的雷暴关系进行分割色块
    colorbar = ax.contourf(lon, lat, K[t_i, :, :], colors=['#000079', '#00AEAE', '#82D900', '#8B2323', '#EE0000'],
                           levels=[0, 293.16, 298.16, 303.16, 308.16, 400],
                           extend='both',
                           transform=ccrs.PlateCarree())
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    titlename = str(time1[t_i]) + '时 K 指数分布场'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()  ###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\ex5picture\\K指数分布图'
    if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()

##Ec 指数
for t_i in range(len(time1)):
    for h_i in range(len(level)):
        ax, fig = createmap()
        colorbar = ax.contourf(lon, lat, Ec[h_i, t_i, :, :], cmap='bwr', transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        titlename = str(time1[t_i]) + str(level[h_i].data) + 'Ec 指数分布场'
        ax.set_title(titlename)
        ax.grid()
        plt.tight_layout()  ###让图填充整个画布
        picturepath = 'D:\\python\\tianzhen\\shixi3_4\\ex5picture\\Ec 指数分布图\\' + str(level[h_i].data)
        if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
            os.makedirs(picturepath)
        picturename = picturepath + '\\' + titlename + '.png'
        plt.savefig(picturename)
        plt.close()
