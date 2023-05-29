from math import *

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np  # 调用 numpy
import pandas as pd
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


###创建地图函数，方便后面调用
def createmap():
    ####生成地图###############################################################################################
    box = [50, 160, 10, 80]  # 经度维度
    scale = '110m'  # 地图分辨率
    xstep = 10  # 下面标注经纬度的步长
    ystep = 10
    proj = ccrs.PlateCarree()  # 确定地图投影
    fig = plt.figure(figsize=(8, 10))  # dpi=150)###生成底图
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  # 确定子图，与 grads 的类似

    ax.set_extent(box, crs=ccrs.PlateCarree())
    ##设置大陆的颜色，1 为白，0 为黑
    # land=cfeat.NaturalEarthFeature('physical','land',scale,edgecolor='face',facecolor=cfeat.COLORS['land'])
    # ax.add_feature(land,facecolor='0.75')
    ##海岸线
    ax.coastlines(scale)
    # 标注坐标轴
    ax.set_xticks(np.arange(box[0], box[1] + xstep, xstep), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(box[2], box[3] + ystep, ystep), crs=ccrs.PlateCarree())
    # 经纬度格式，把 0 经度设置不加 E 和 W
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ############################################################################################################
    return ax, fig


upfrist = ['air', 'hgt', 'uv']
var = ['air', 'hgt', 'u', 'v']
frist = ['1000', '925', '850', '700', '600', '500']
second = ['2021052000', '2021052006', '2021052012', '2021052018', '2021052100', '2021052106', '2021052112',
          '2021052118', '2021052200', '2021052206', '2021052212', '2021052218', '2021052300', '2021052306',
          '2021052312', '2021052318', '2021052400']

a = np.full((len(var), len(second), len(frist), 29, 45), -99.9)  # 创建一个五维数组

##############################################读取数据##################################################################
for k in upfrist:
    for i in frist:
        for j in second:
            filename = 'D:\\python\\tianzhen\\shixi2\\' + k + '\\' + i + '\\' + j + '.txt'
            f = open(filename, 'r', encoding='UTF-8')
            if k != 'uv':  # 读取气温，位势高度

                for bb in range(4):  # 提前读取，跳过前四行
                    b = f.readline()

                for y_i in range(28, -1, -1):
                    x_i = 0

                    for bbb in range(5):
                        List = f.readline()
                        list_start = 2  # 字符串截取起始
                        list_end = 11  # 字符串截取结束

                        for x in range(10):
                            a[upfrist.index(k), second.index(j), frist.index(i), y_i, x_i] = float(
                                List[list_start:list_end:1])
                            list_start += 10  # 跳到下一个数据的两侧
                            list_end += 10
                            x_i += 1
                            if x_i == 45:  # 第五行只有五个数据，设置提前跳出循环
                                break
            else:  # 读取 uv 风场
                for bb in range(3):
                    b = f.readline()
                for var_i in range(2, 4):
                    for y_i in range(28, -1, -1):
                        x_i = 0  # 数据纬向存储（按列）

                        for bbb in range(5):
                            List = f.readline()
                            list_start = 2  # 字符串截取起始
                            list_end = 11  # 字符串截取结束

                            for x in range(10):
                                a[var_i, second.index(j), frist.index(i), y_i, x_i] = float(
                                    List[list_start:list_end:1])
                                list_start += 10  # 跳到下一个数据的两侧
                                list_end += 10
                                x_i += 1
                                if x_i == 45:
                                    break
#######################################存放数据到 nc 文件，方便后面画图#######################################################
time = pd.date_range(start='20210520', end='20210524', periods=17)
level = np.array([1000, 925, 850, 700, 600, 500], dtype=float)
lat = np.arange(10, 81, 2.5)
lon = np.arange(50, 161, 2.5)

air = a[0, :, :, :, :]
hgt = a[1, :, :, :, :]
u = a[2, :, :, :, :]
v = a[3, :, :, :, :]
all_vars = xr.Dataset({'air': (['time', 'level', 'lat', 'lon'], air),
                       'hgt': (['time', 'level', 'lat', 'lon'], hgt),
                       'u': (['time', 'level', 'lat', 'lon'], u),
                       'v': (['time', 'level', 'lat', 'lon'], v)},

                      coords={'lon': (['lon'], lon),
                              'lat': (['lat'], lat),
                              'time': (['time'], time),
                              'level': (['level'], level)
                              })
all_vars.to_netcdf('D:\\python\\tianzhen\\shixi2\\all.nc')
##############################################计算部分##################################################################
# 定义一些常量
omega = 7.272 * 10 ** (-5)  # 地转角速度
r = 6371  # 地球半径
g = 9.8  # 重力加速度
dx = 2.5 * pi / 180  # 网格距
dy = 2.5 * pi / 180  # 网格距
# 问题一:500hPa 地转风涡度，实测风涡度平流，温度平流 24 小时变高
##地转风涡度
gv_500 = np.full((17, 29, 45), -9.99 * exp(-6))  # 每一时次 500hPa 地转风涡度
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            gv_500[time, j, i] = g / (2 * omega * sin((10 + dy * j) * pi / 180) * r ** 2) * (
                    (a[1, time, 5, j, i + 1] + a[1, time, 5, j, i - 1] - 2 * a[1, time, 5, j, i]) / (
                    dx ** 2 * cos((10 + dy * j) * pi / 180) ** 2) + (a[1, time, 5, j + 1, i] + a[1, time, 5, j - 1, i]
                                                                     - 2 * a[1, time, 5, j, i]) / (dy ** 2) - (
                            a[1, time, 5, j + 1, i] - a[1, time, 5, j - 1, i])
                    * tan((10 + dy * j) * pi / 180) / (2 * dy))  # 计算公式
###实测风涡度
mwv_500 = np.full((17, 29, 45), -9.99 * exp(-6))  # 每一时次的实测风涡度
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            mwv_500[time, j, i] = 1 / (2 * r) * (
                    (a[3, time, 5, j, i + 1] - a[3, time, 5, j, i - 1]) / (cos((10 + dy * j) * pi / 180) * dx) - (
                    a[2, time, 5, j + 1, i] - a[2, time, 5, j - 1, i]) / dy + 2 * a[2, time, 5, j, i] * tan(
                (10 + dy * j) * pi / 180))  # 公式
## 实测风涡度平流
dtx = np.full((17, 29, 45), -9.99 * exp(-6))  # 参考 grads cdiff() 函数 纬向中央差分
dty = np.full((17, 29, 45), -9.99 * exp(-6))  # 经向中央差分
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            dtx[time, j, i] = ((mwv_500[time, j, i + 1] - mwv_500[time, j, i - 1]) / 2)
            dty[time, j, i] = ((mwv_500[time, j + 1, i] - mwv_500[time, j - 1, i]) / 2)
mwv_500_adv = np.full((17, 29, 45), -9.99 * exp(-6))  # 实测风涡度平流
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            mwv_500_adv[time, j, i] = -(
                    (a[2, time, 5, j, i] * dtx[time, j, i]) / (dx * cos((10 + dy * j) * pi / 180)) + (
                    a[3, time, 5, j, i] * dty[time, j, i]) / dy) / r  # 公式
###温度平流
air_500_adv = np.full((17, 29, 45), -9.99 * exp(-6))
dtx = np.full((17, 29, 45), -9.99 * exp(-6))  # 参考 grads cdiff() 函数 纬向中央差分
dty = np.full((17, 29, 45), -9.99 * exp(-6))  # 经向中央差分
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            dtx[time, j, i] = (a[0, time, 5, j, i + 1] - a[0, time, 5, j, i - 1]) / 2
            dty[time, j, i] = (a[0, time, 5, j + 1, i] - a[0, time, 5, j - 1, i]) / 2
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            air_500_adv[time, j, i] = -(
                    (a[2, time, 5, j, i] * dtx[time, j, i]) / (dx * cos((10 + dy * j) * pi / 180)) + (
                    a[3, time, 5, j, i] * dty[time, j, i]) / dy) / r  # 公式
###24 小时变高
hgt_500_24change_all = np.full((4, 29, 45), 0)
i = 0
for time in range(0, 17, 4):
    if time == 16:
        break
    hgt_500_24change_all[i, :, :] = a[1, time + 4, 5, :, :] - a[1, time, 5, :, :]
    i = i + 1

######问题二:850hPa 实测风涡度，散度，24 小时变高，6 小时变温，1000hPa24 小时变温
##实测风涡度
mwv_850 = np.full((17, 29, 45), -9.99 * exp(-6))  # 每一时次的实测风涡度
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            mwv_850[time, j, i] = 1 / (2 * r) * (
                    (a[3, time, 2, j, i + 1] - a[3, time, 2, j, i - 1]) / (cos((10 + dy * j) * pi / 180) * dx) - (
                    a[2, time, 2, j + 1, i] - a[2, time, 2, j - 1, i]) / dy + 2 * a[2, time, 2, j, i] * tan(
                (10 + dy * j) * pi / 180))

##散度
d_850 = np.full((17, 29, 45), -9.99 * exp(-6))  # 每一时次
for time in range(17):
    for i in range(45):
        if i == 0 or i == 44:
            continue
        for j in range(29):
            if j == 0 or j == 28:
                continue
            d_850[time, j, i] = 1 / (2 * r) * ((a[2, time, 2, j, i + 1] - a[2, time, 2, j, i - 1]) / (
                    dx * cos((10 + dy * j) * pi / 180)) + (a[3, time, 2, j + 1, i] - a[3, time, 2, j - 1, i]) / dy - 2 *
                                               a[3, time, 2, j, i] * tan((10 + dy * j) * pi / 180))  # 公式

##24 小时变高变温
hgt_850_24change_all = np.full((4, 29, 45), 0)
air_850_24change_all = np.full((4, 29, 45), 0)
i = 0
for time in range(0, 17, 4):
    if time == 16:
        break
    hgt_850_24change_all[i, :, :] = a[1, time + 4, 2, :, :] - a[1, time, 2, :, :]
    air_850_24change_all[i, :, :] = a[0, time + 4, 2, :, :] - a[0, time, 2, :, :]
    i = i + 1

##6 小时变温
air_850_6change_all = np.full((16, 29, 45), 0)
i = 0
for time in range(17):
    if time == 16:
        break
    air_850_6change_all[i, :, :] = a[0, time + 1, 2, :, :] - a[0, time, 2, :, :]
    i = i + 1

##1000hPa 24 小时变温
air_1000_24change_all = np.full((4, 29, 45), 0)
i = 0
for time in range(0, 17, 4):
    if time == 16:
        break
    air_1000_24change_all[i, :, :] = a[0, time + 4, 0, :, :] - a[0, time, 0, :, :]
    i = i + 1

############################################画图#######################################################################
#####问题三：绘制 500hPa 温压场配置
plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
air_hgt = xr.open_dataset('D:\\python\\tianzhen\\shixi2\\all.nc')
lat = air_hgt['lat'][:]
lon = air_hgt['lon'][:]
lons, lats = np.meshgrid(lon, lat)  # 后面画图数据对应

###绘制 500hPa 温压场 17 个时刻
for t_i in second:
    ax, fig = createmap()
    ####读取数据
    plot_air_500 = air_hgt['air'][second.index(t_i), 5, :, :]  #
    plot_hgt_500 = air_hgt['hgt'][second.index(t_i), 5, :, :]  #

    air_levels = np.arange(-100, 20, 4)  # 设置等值线间隔
    hgt_levels = np.arange(400, 600, 4)
    # 绘制等值线
    denghgtlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_hgt_500[0:28, 0:44], levels=hgt_levels,
                              colors='mediumblue', linewidths=0.8)  #
    plt.clabel(denghgtlines, inline=True, fontsize=8, fmt='%.0f')
    dengairlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_air_500[0:28, 0:44], levels=air_levels,
                              colors='red', linewidths=0.8)  #
    plt.clabel(dengairlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 500hPa 温压场'  #
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question3\\' + t_i  #
    fig.savefig(picturename)  # 保存图片
    plt.close(fig)

######绘制问题一的图，500hPa 地转风涡度，实测风涡度平流，温度平流，24 小时变高
# 地转风涡度
for t_i in second:
    ax, fig = createmap()
    ###读取数据，
    gv = gv_500[second.index(t_i), :, :]
    # 设置等值线间隔
    gv_levels = np.arange(-100, 100, 4)
    denggvlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], gv[0:28, 0:44], levels=gv_levels,
                             cmap='viridis', linewidths=0.8)
    plt.clabel(denggvlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 500hPa 地转风涡度'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question1\\500hPagvpicture\\' + t_i
    fig.savefig(picturename)  # 保存图片
    plt.close(fig)
# 实测风涡度平流
for t_i in second:
    ax, fig = createmap()
    ###读取数据
    mwv = mwv_500_adv[second.index(t_i), :, :] * 10 ** 4
    # 设置等值线间隔
    mwv_levels = np.arange(-100, 100, 3)
    dengmwvlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], mwv[0:28, 0:44], levels=mwv_levels,
                              cmap='viridis', linewidths=0.8)
    plt.clabel(dengmwvlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 500hPa 实测风涡度平流'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question1\\500hPamwvadvpicture\\' + t_i
    fig.savefig(picturename)  ##保存图片
    plt.close(fig)
# 温度平流
for t_i in second:
    ax, fig = createmap()
    ###读取数据
    air = air_500_adv[second.index(t_i), :, :] * 10 ** 2
    ###设置等值线间隔
    air_levels = np.arange(-100, 100, 3)
    dengairlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], air[0:28, 0:44], levels=air_levels,
                              cmap='viridis', linewidths=0.8)
    plt.clabel(dengairlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 500hPa 温度平流'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question1\\500hPaairadvpicture\\' + t_i
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 24 小时变高
for i in range(4):
    ax, fig = createmap()
    hgt24change = hgt_500_24change_all[i, :, :]
    ###设置等值线间隔
    hgt24change_levels = np.arange(-100, 100, 4)
    deng24changelines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], hgt24change[0:28, 0:44],
                                   levels=hgt24change_levels,
                                   cmap='viridis', linewidths=0.4)
    plt.clabel(deng24changelines, inline=True, fontsize=8, fmt='%.0f')
    titlename = '2' + str(i) + '-' + '2' + str(i + 1) + '日 500hPa24 小时变高'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question1\\500hPahgt24changepicture\\' + titlename
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
#####绘制问题二的图 500hPa 实测风涡度和散度，24 小时变温变高，6 小时变温，1000hPa24 小时变温
# 实测风涡度
for t_i in second:
    ax, fig = createmap()
    ###读取数据
    mwv = mwv_850[second.index(t_i), :, :] * 10 ** 3
    ###设置等值线间隔
    mwv_levels = np.arange(-100, 100, 8)
    dengmwvlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], mwv[0:28, 0:44], levels=mwv_levels,
                              cmap='viridis', linewidths=0.8)
    plt.clabel(dengmwvlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 850hPa 实测风涡度'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\850hPamwvpicture\\' + t_i
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 散度
for t_i in second:
    ax, fig = createmap()
    ###读取数据
    d = d_850[second.index(t_i), :, :] * 10 ** 3
    ###设置等值线间隔
    d_levels = np.arange(-100, 100, 4)
    dengdlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], d[0:28, 0:44], levels=d_levels,
                            cmap='viridis', linewidths=0.4)
    plt.clabel(dengdlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 850hPa 散度'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\850hPadpicture\\' + t_i
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 24 小时变高
for i in range(4):
    ax, fig = createmap()
    hgt24change = hgt_850_24change_all[i, :, :]
    ###设置等值线间隔
    hgt24change_levels = np.arange(-100, 100, 2)
    deng24changelines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], hgt24change[0:28, 0:44],
                                   levels=hgt24change_levels,
                                   cmap='viridis', linewidths=0.4)
    plt.clabel(deng24changelines, inline=True, fontsize=8, fmt='%.0f')
    titlename = '2' + str(i) + '-' + '2' + str(i + 1) + '日 850hPa24 小时变高'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\850hPahgt24changepicture\\' + titlename
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 24 小时变温
for i in range(4):
    ax, fig = createmap()
    air24change = air_850_24change_all[i, :, :]
    ###设置等值线间隔
    air24change_levels = np.arange(-100, 100, 3)
    deng24changelines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], air24change[0:28, 0:44],
                                   levels=air24change_levels,
                                   cmap='viridis', linewidths=0.4)
    plt.clabel(deng24changelines, inline=True, fontsize=8, fmt='%.0f')
    titlename = '2' + str(i) + '-' + '2' + str(i + 1) + '日 850hPa24 小时变温'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\850hPaair24changepicture\\' + titlename
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 6 小时变温
for i in range(16):
    ax, fig = createmap()
    air6change = air_850_6change_all[i, :, :]
    ###设置等值线间隔
    air6change_levels = np.arange(-100, 100, 1)
    deng6changelines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], air6change[0:28, 0:44], levels=air6change_levels,
                                  cmap='viridis', linewidths=0.4)
    plt.clabel(deng6changelines, inline=True, fontsize=8, fmt='%.0f')
    titlename = str(i) + '850hPa6 小时变温'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\850hPaair6changepicture\\' + titlename
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
# 1000hPa 24 小时变温
for i in range(4):
    ax, fig = createmap()
    air24change = air_1000_24change_all[i, :, :]
    ###设置等值线间隔
    air24change_levels = np.arange(-100, 100, 2)
    deng24changelines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], air24change[0:28, 0:44],
                                   levels=air24change_levels,
                                   cmap='viridis', linewidths=0.4)
    plt.clabel(deng24changelines, inline=True, fontsize=8, fmt='%.0f')
    titlename = '2' + str(i) + '-' + '2' + str(i + 1) + '日 1000hPa24 小时变温'
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question2\\1000hPaair24changepicture\\' + titlename
    fig.savefig(picturename)  ## 保存图片
    plt.close(fig)
#####问题四，为问题四绘制 1000hPa，850hPa 温压场
# 1000hPa 温压场
for t_i in second:
    ax, fig = createmap()
    ####读取数据
    plot_air_1000 = air_hgt['air'][second.index(t_i), 0, :, :]  #
    plot_hgt_1000 = air_hgt['hgt'][second.index(t_i), 0, :, :]  #

    air_levels = np.arange(-100, 100, 4)  # 设置等值线间隔
    hgt_levels = np.arange(-1000, 1500, 4)  #
    # 绘制等值线
    denghgtlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_hgt_1000[0:28, 0:44], levels=hgt_levels,
                              colors='mediumblue', linewidths=0.8)  #
    plt.clabel(denghgtlines, inline=True, fontsize=8, fmt='%.0f')
    dengairlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_air_1000[0:28, 0:44], levels=air_levels,
                              colors='red', linewidths=0.8)  #
    plt.clabel(dengairlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 1000hPa 温压场'  #
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question4\\1000\\' + t_i  #
    fig.savefig(picturename)  # 保存图片
    plt.close(fig)
# 850hPa 温压场
for t_i in second:
    ax, fig = createmap()
    ####读取数据
    plot_air_850 = air_hgt['air'][second.index(t_i), 2, :, :]  #
    plot_hgt_850 = air_hgt['hgt'][second.index(t_i), 2, :, :]  #

    air_levels = np.arange(-100, 100, 4)  # 设置等值线间隔
    hgt_levels = np.arange(-1000, 1500, 4)  #
    # 绘制等值线
    denghgtlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_hgt_850[0:28, 0:44], levels=hgt_levels,
                              colors='mediumblue', linewidths=0.8)  #
    plt.clabel(denghgtlines, inline=True, fontsize=8, fmt='%.0f')
    dengairlines = ax.contour(lons[0:28, 0:44], lats[0:28, 0:44], plot_air_850[0:28, 0:44], levels=air_levels,
                              colors='red', linewidths=0.8)  #
    plt.clabel(dengairlines, inline=True, fontsize=8, fmt='%.0f')
    titlename = t_i + '时 850hPa 温压场'  #
    ax.set_title(titlename, fontsize=12)
    ax.grid()
    picturename = 'D:\\python\\tianzhen\\shixi2\\question4\\850\\' + t_i  #
    fig.savefig(picturename)  # 保存图片
    plt.close(fig)
#####################
