from math import *

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np  # 调用numpy
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from xgrads import *


# %%
def createmap():  ###############################################生成地图##########################################################
    box = [-180, 180, -90, 90]  # 经度维度
    scale = '110m'  # 地图分辨率
    xstep = 20  # 下面标注经纬度的步长
    ystep = 10
    proj = ccrs.PlateCarree()  # 确定地图投影
    fig = plt.figure(figsize=(9, 6))  # dpi=150)###生成底图
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})  # 确定子图，与grads的类似
    ##海岸线
    ax.coastlines(scale)
    # 标注坐标轴
    ax.set_xticks(np.arange(box[0], box[1] + xstep, xstep), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(box[2], box[3] + ystep, ystep), crs=ccrs.PlateCarree())
    # 经纬度格式，把0经度设置不加E和W
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ############################################################################################################
    return ax, fig


# %%
plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
plt.rcParams['axes.unicode_minus'] = False  ###用来正常显示负号
# %%
air = open_CtlDataset('D:\\grads\\TongJi\\HADISST_50y.ctl')
air.attrs['pdef'] = 'None'
air.to_netcdf('D:\\grads\\TongJi\\HADISST_50y.nc')
air = xr.open_dataset('D:\\grads\\TongJi\\HADISST_50y.nc')
# %%
air
# %%
lonstart = 215
lonend = 307
latstart = 70
latend = 112
sst = air['sst'][:, latstart:latend, lonstart:lonend]
sst_global = air['sst'][:, :, :]
time = air['time'][:]
lon = air['lon'][lonstart:lonend]
lon1 = air['lon'][:]
lat = air['lat'][latstart:latend]
lat1 = air['lat'][:]
# %%
sumsst = np.zeros((len(lat), len(lon)))
sumxt = np.zeros((len(lat), len(lon)))
sst_shijian = np.zeros((len(time)))
# %%
avesst_global = np.zeros((len(time), len(lat1), len(lon1)))
sst_global = sst_global.where(sst_global > -999, np.NAN)
avesst_global = sst_global.mean(dim='time', skipna=True)
# %%
avesst_global
# %%
##印度洋海温
for time_i in range(len(time)):
    a = []
    for i in range(len(lon)):
        for j in range(len(lat)):
            if float(sst[time_i, j, i]) != -999:
                a.append(float(sst[time_i, j, i]))
    sst_shijian[time_i] = sum(a) / len(a)
# %%
t = np.arange(1958, 2008, 1)
# %%
avet = sum(t) / len(t)
avesst_shijian = sum(sst_shijian) / len(sst_shijian)
t2 = t * t
# %%
sumxt = np.zeros((len(time)))
for time_i in range(len(time)):
    sumxt[time_i] = sst_shijian[time_i] * t[time_i]
# %%
##全球的海温的线性估计
sumxt1 = np.zeros((len(time), len(lat1), len(lon1)))
for time_i in range(len(time)):
    sumxt1[time_i, :, :] = sst_global[time_i, :, :] * t[time_i]
b1 = (sum(sumxt1) - len(time) * avesst_global * avet) / (sum(t2) - len(time) * pow(avet, 2))
# %%
# 线性倾向估计
b = (sum(sumxt) - len(time) * avesst_shijian * avet) / (sum(t2) - len(time) * pow(avet, 2))
# %%
a = avesst_shijian - b * avet
# %%
y = a + b * t
r = sqrt(
    (sum(t2) - len(time) * pow(avet, 2)) / (sum(sst_shijian * sst_shijian) - len(time) * pow(avesst_shijian, 2))) * b
# %%
# 取滑动长度为五
k = 5
y_huandong = np.zeros((len(time) - k + 1))
for time_i in range(len(time) - k + 1):
    a = 0
    for k_i in range(k):
        a = a + sst_shijian[k_i + time_i - 1]
    y_huandong[time_i] = a / k
# %%
# 累计平均
y_leijiJuPing = np.zeros((len(time)))
for time_i in range(len(time)):
    a = 0
    for t_i in range(time_i + 1):
        a = a + sst_shijian[t_i] - avesst_shijian
    y_leijiJuPing[time_i] = a
# %%
##问题一
fig = plt.figure(figsize=(16, 9))
ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=2)
ax2 = plt.subplot2grid((5, 1), (2, 0), rowspan=3)
ax1.set_xticks(range(1960, 2008, 5))
ax1.xaxis.tick_top()
ax1.set_ylim(26, 29)
ax1.plot(t, y, label='r= ' + str(r))
ax1.plot(t[:len(time) - k + 1], y_huandong, linestyle='-.', label='k=' + str(k) + '的滑动平均', alpha=0.75)
ax1.plot(t, sst_shijian, label='印度洋区域平均海温时间序列', alpha=0.5)
ax1.legend()
ax2.set_xticks(range(1960, 2008, 5))
ax2.set_ylim(-5, 0)
ax2.plot(t, y_leijiJuPing, color='r', marker='v', mec='g', label='累计距平')
ax2.legend()
plt.subplots_adjust(hspace=0)
plt.savefig('D:\\grads\\TongJi\\ex5\\1.png')
plt.show()
plt.close()
# %%
##问题二全球海温变化趋势
# lon1,lat1=np.meshgrid(lon1,lat1)
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b1, cmap='jet', tranform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
ax.set_title('全球海温变化趋势')
# plt.tight_layout()
plt.savefig(r'D:\grads\TongJi\ex5\3.png')
plt.close()
