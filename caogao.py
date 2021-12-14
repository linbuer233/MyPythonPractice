from xgrads import *
import numpy as np  # 调用numpy
import xarray as xr
from math import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def createmap():
    ###############################################生成地图##########################################################
    box = [-180, 180, -90, 90]  # 经度维度
    scale = '110m'  # 地图分辨率
    xstep = 20  # 下面标注经纬度的步长
    ystep = 10
    proj = ccrs.PlateCarree(central_longitude=180)  # 确定地图投影
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


air = xr.open_dataset('D:\\grads\\TongJi\\NCEP_Z200_30y_Wt.nc')
# air = xr.open_dataset('D:\\grads\\TongJi\\NCEP_TPSST_30y_Wt.nc')

st1 = air['hgt'][8, :, :]
lon = air['lon'][:]
lat = air['lat'][:]

ax, fig = createmap()
a=ax.contour(lon, lat, st1,levels=np.arange(11000,100000,200),
                extend='both',
               transform=ccrs.PlateCarree())
plt.clabel(a, inline=True, fontsize=8, fmt='%.0f')
plt.show()
