'''
实习四：是利用同一套资料计算
（1）流函数和势函数；
（2）水汽通量和水汽通量散度；
（3）水汽流函数和水汽势函数。
2021/11/7
'''

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import metpy.calc as mpcalc
import metpy.constants
import numpy as np  # 调用 numpy
import pandas as pd
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


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


shi_han_shu = np.load(r'D:\python\tianzhen\shixi3_4\势函数.npy')
c = np.zeros((24, 12, 29, 73))
b = np.array(shi_han_shu)
for h_i in range(12):
    for t_i in range(24):
        c[t_i, h_i, :, :] = b[t_i, h_i, :, :].T

lons = np.arange(0, 181, 2.5)
lats = np.arange(10, 81, 2.5)
lon, lat = np.meshgrid(lons, lats)

for h_i in range(12):
    for t_i in range(24):
        ax, fig = createmap()
        colorbar = ax.contourf(lon, lat, c[t_i, h_i, :, :], cmap='Spectral', transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        name = 'D:\\python\\tianzhen\\shixi3_4\\ex4\\势函数\\' + str(h_i) + '_' + str(t_i) + '.png'
        plt.savefig(name)
        plt.close()

shi_han_shu = np.load(r'D:\python\tianzhen\shixi3_4\水汽势函数.npy')
c = np.zeros((24, 8, 29, 73))
b = np.array(shi_han_shu)
for h_i in range(8):
    for t_i in range(24):
        c[t_i, h_i, :, :] = b[t_i, h_i, :, :].T
for h_i in range(8):
    for t_i in range(24):
        ax, fig = createmap()
        colorbar = ax.contourf(lon, lat, c[t_i, h_i, :, :], cmap='Spectral', transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        name = 'D:\\python\\tianzhen\\shixi3_4\\ex4\\水汽势函数\\' + str(h_i) + '_' + str(t_i) + '.png'
        plt.savefig(name)
        plt.close()
liu_han_shu = np.load(r'D:\python\tianzhen\shixi3_4\流函数.npy')
shuiqi_liu_han_shu = np.load(r'D:\python\tianzhen\shixi3_4\水汽流函数.npy')
uwind = np.load(r'D:\python\tianzhen\shixi3_4\水汽通量u分量.npy')
vwind = np.load(r'D:\python\tianzhen\shixi3_4\水汽通量v分量.npy')
liu_hanshu = np.zeros((24, 12, 29, 73))
shuiqiliu_hanshu = np.zeros((24, 8, 29, 73))
liuhanshu_array = np.array(liu_han_shu)
shuiqiliuhanshu_array = np.array(shuiqi_liu_han_shu)
for h_i in range(8):
    for t_i in range(24):
        shuiqiliu_hanshu[t_i, h_i, :, :] = shuiqiliuhanshu_array[t_i, h_i, :, :].T
for h_i in range(12):
    for t_i in range(24):
        liu_hanshu[t_i, h_i, :, :] = liuhanshu_array[t_i, h_i, :, :].T
##流函数
for h_i in range(8):
    for t_i in range(24):
        ax, fig = createmap()
        colorbar = ax.contourf(lon, lat, liu_hanshu[t_i, h_i, :, :], cmap='Spectral', transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        plt.quiver(lon, lat, uwind[h_i, t_i, :, :], vwind[h_i, t_i, :, :], transform=ccrs.PlateCarree())
        name = 'D:\\python\\tianzhen\\shixi3_4\\ex4\\流函数\\' + str(h_i) + '_' + str(t_i) + '.png'
        plt.savefig(name)
        plt.close()
##水汽流函数
for h_i in range(8):
    for t_i in range(24):
        ax, fig = createmap()
        colorbar = ax.contourf(lon, lat, shuiqiliu_hanshu[t_i, h_i, :, :], cmap='Spectral',
                               transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        plt.quiver(lon, lat, uwind[h_i, t_i, :, :], vwind[h_i, t_i, :, :], transform=ccrs.PlateCarree())
        name = 'D:\\python\\tianzhen\\shixi3_4\\ex4\\水汽流函数\\' + str(h_i) + '_' + str(t_i) + '.png'
        plt.savefig(name)
        plt.close()
