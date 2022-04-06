import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.io.shapereader import Reader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
plt.rcParams['axes.unicode_minus'] = False  ###用来正常显示负号

air_hgt_500 = xr.open_dataset('D:\\python\\tianzhen\\shixi2\\all.nc')
lat = air_hgt_500['lat'][:]
lon = air_hgt_500['lon'][:]
lons, lats = np.meshgrid(lon, lat)

###################################地图设置##########################
proj = ccrs.LambertConformal(central_longitude=105, central_latitude=30)
leftlon, rightlon, lowerlat, upperlat = (50, 160, 10, 80)
fig = plt.figure(figsize=(9, 6))  # 画布大小
ax = fig.subplots(1, 1, subplot_kw={'projection': ccrs.LambertConformal(central_longitude=105, central_latitude=30)})

path = mpath.Path([[leftlon, lowerlat], [rightlon, lowerlat], [rightlon, upperlat], [leftlon, upperlat],
                   [leftlon, lowerlat]]).interpolated(20)  ###设置地图边界
# transpath = (ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData).transform_path(path)
# ax.set_boundary(transpath)
# 经纬度格式，把0经度设置不加E和W
lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.set_extent([50, 160, 10, 80])  ## 调整图片大小在画布中
ax.add_feature(cfeature.COASTLINE.with_scale('110m'))
ax.gridlines(draw_labels=True, x_inline=False, y_inline=False)
ax.add_geometries(Reader('D:\\maplist\\China_province\\bou2_4l.shp').geometries(), ccrs.PlateCarree(),
                  facecolor='none', edgecolor='gray', linewidth=0.8)  ###添加省界
#####################################
uwind = np.zeros((29, 45))
vwind = np.zeros((29, 45))
plot_air_500 = air_hgt_500['air'][0, 5, :, :]
plot_hgt_500 = air_hgt_500['hgt'][0, 5, :, :]
uwind[:, :] = air_hgt_500['u'][0, 5, :, :]
vwind[:, :] = air_hgt_500['v'][0, 5, :, :]

air_levels = np.arange(-100, 20, 4)  # 设置等值线间隔
hgt_levels = np.arange(400, 600, 4)
#############画等值线图##################
denghgtlines = ax.contour(lon, lat, plot_hgt_500, levels=hgt_levels,
                          colors='mediumblue', linewidths=0.8, transform=ccrs.PlateCarree())
plt.clabel(denghgtlines, inline=True, fontsize=8, fmt='%.0f'
           )
dengairlines = ax.contour(lon, lat, plot_air_500, levels=air_levels,
                          colors='red', linewidths=0.8, linestyles='-', transform=ccrs.PlateCarree())
plt.clabel(dengairlines, inline=True, fontsize=8, fmt='%.0f')
#############https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html#matplotlib.pyplot.contour

######################################################画风羽图##################################################
wind_slice = (slice(None, None, 2), slice(None, None, 2))  ####调风羽的密度
plt.barbs(lons[wind_slice], lats[wind_slice], uwind[wind_slice], vwind[wind_slice], pivot='middle', length=4,
          color='black', barb_increments=dict(half=2, full=4, flag=20), transform=ccrs.PlateCarree())

#########[x,y,u,v]  这四个都要 ndarray 形式
######### https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barbs.html#matplotlib.pyplot.barbs
ax.set_title('2021-05-20 00时500hPa温压场', fontsize=12)

gl = ax.gridlines()  ##生成网格线
ax.grid()
plt.show()
fig.savefig('d:\\python\\hh')
