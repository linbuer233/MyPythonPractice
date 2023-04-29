import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np  # 调用numpy
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from xgrads import *


def createmap():
    ###############################################生成地图##########################################################
    box = [-180, 180, -90, 90]  # 经度维度
    scale = '110m'  # 地图分辨率
    xstep = 20  # 下面标注经纬度的步长
    ystep = 10
    proj = ccrs.PlateCarree(central_longitude=0)  # 确定地图投影
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


############NCEP_Z200_30y_Wt转换成nc文件############
hgt = open_CtlDataset('D:\\grads\\TongJi\\NCEP_Z200_30y_Wt.ctl')
hgt.attrs['pdef'] = 'None'
hgt.to_netcdf('D:\\grads\\TongJi\\NCEP_Z200_30y_Wt.nc')
hgt = xr.open_dataset('D:\\grads\\TongJi\\NCEP_Z200_30y_Wt.nc')
############NCEP_TPSST_30y_Wt转换成nc文件###########
air = open_CtlDataset('D:\\grads\\TongJi\\NCEP_TPSST_30y_Wt.ctl')
air.attrs['pdef'] = 'None'
air.to_netcdf('D:\\grads\\TongJi\\NCEP_TPSST_30y_Wt.nc')
air = xr.open_dataset('D:\\grads\\TongJi\\NCEP_TPSST_30y_Wt.nc')
###########NCEP_IOSST_30y_Wt转换成nc文件###########
airindia = open_CtlDataset('D:\\grads\\TongJi\\NCEP_IOSST_30y_Wt.ctl')
airindia.attrs['pdef'] = 'None'
airindia.to_netcdf('D:\\grads\\TongJi\\NCEP_IOSST_30y_Wt.nc')
airindia = xr.open_dataset('D:\\grads\\TongJi\\NCEP_IOSST_30y_Wt.nc')

#####热带太平洋海温
lon = air['lon'][:]
lat = air['lat'][:]
st1 = air['st'][4, :, :]
st2 = air['st'][8, :, :]
st3 = air['st'][13, :, :]
st4 = air['st'][19, :, :]
st5 = air['st'][24, :, :]
st1_new = []
st2_new = []
st3_new = []
st4_new = []
st5_new = []
for i in range(len(lon)):
    for j in range(len(lat)):
        if float(st1[j, i]) < 9999:
            st1_new.append(float(st1[j, i]))
        if float(st2[j, i]) < 9999:
            st2_new.append(float(st2[j, i]))
        if float(st3[j, i]) < 9999:
            st3_new.append(float(st3[j, i]))
        if float(st4[j, i]) < 9999:
            st4_new.append(float(st4[j, i]))
        if float(st5[j, i]) < 9999:
            st5_new.append(float(st5[j, i]))
avest1 = sum(st1_new) / (len(st1_new))
avest2 = sum(st2_new) / (len(st2_new))
avest3 = sum(st3_new) / (len(st3_new))
avest4 = sum(st4_new) / (len(st4_new))
avest5 = sum(st5_new) / (len(st5_new))
###印度太平洋海温###
lon2 = airindia['lon'][:]
lat2 = airindia['lat'][:]
st_india1 = airindia['st'][4, :, :]
st_india2 = airindia['st'][8, :, :]
st_india3 = airindia['st'][13, :, :]
st_india4 = airindia['st'][19, :, :]
st_india5 = airindia['st'][24, :, :]
st_india1_new = []
st_india2_new = []
st_india3_new = []
st_india4_new = []
st_india5_new = []
for i in range(len(lon2)):
    for j in range(len(lat2)):
        if float(st_india1[j, i]) < 9999:
            st_india1_new.append(float(st_india1[j, i]))
        if float(st_india2[j, i]) < 9999:
            st_india2_new.append(float(st_india2[j, i]))
        if float(st_india3[j, i]) < 9999:
            st_india3_new.append(float(st_india3[j, i]))
        if float(st_india4[j, i]) < 9999:
            st_india4_new.append(float(st_india4[j, i]))
        if float(st_india5[j, i]) < 9999:
            st_india5_new.append(float(st_india5[j, i]))
avest_india1 = sum(st_india1_new) / (len(st_india1_new))
avest_india2 = sum(st_india2_new) / (len(st_india2_new))
avest_india3 = sum(st_india3_new) / (len(st_india3_new))
avest_india4 = sum(st_india4_new) / (len(st_india4_new))
avest_india5 = sum(st_india5_new) / (len(st_india5_new))

###200hPa位势高度场
time = hgt['time'][:]
lon1 = hgt['lon'][:]
lat1 = hgt['lat'][:]
hgt1 = hgt['hgt'][4, :, :]
hgt2 = hgt['hgt'][8, :, :]
hgt3 = hgt['hgt'][13, :, :]
hgt4 = hgt['hgt'][19, :, :]
hgt5 = hgt['hgt'][24, :, :]
avehgt = (hgt1 + hgt2 + hgt3 + hgt4 + hgt5) / 5

avest = (avest1 + avest2 + avest3 + avest4 + avest5) / 5
avest_india = (avest_india1 + avest_india2 + avest_india3 + avest_india4 + avest_india5) / 5

ax, fig = createmap()
colorbar = ax.contour(lon1, lat1, hgt1 * avest1, cmap='bwr', levels=np.arange(300000, 10000000, 5000),
                      transform=ccrs.PlateCarree())
plt.clabel(colorbar, inline=True, fontsize=8, fmt='%.0f')
plt.tight_layout()
# plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.show()
'''
###多元回归
stTP = np.array([avest1, avest2, avest3, avest4, avest5])
stindia = np.array([avest_india1, avest_india2, avest_india3, avest_india4, avest_india5])
hgtZ200 = np.array([hgt1, hgt2, hgt3, hgt4, hgt5])
a = np.full((5, 1), 1)
X = np.array([[5, sum(stTP), sum(stindia)],
              [sum(stTP), sum(stTP * stTP), sum(stTP * stindia)],
              [sum(stindia), sum(stTP * stindia), sum(stindia * stindia)]])
y1 = np.zeros((len(lat1), len(lon1)))
y2 = np.zeros((len(lat1), len(lon1)))
y = np.zeros((len(lat1), len(lon1)))
for i in range(5):
    y1 += hgtZ200[i, :, :] * stTP[i]
    y2 += hgtZ200[i, :, :] * stindia[i]
    y += hgtZ200[i, :, :]
Y = np.array([y, y1, y2])
X1 = np.linalg.inv((X.T).dot(X)).dot(X.T)
b = np.zeros((3, len(lat1), len(lon1)))
for i in range(len(lon1)):
    for j in range(len(lat1)):
        b[:, j, i] = X1.dot(Y[:, j, i])
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b[1, :, :], cmap='bwr',
                       transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex42bTPSST.png')
plt.close()
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b[2, :, :], cmap='bwr',
                       transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex42bIOSST.png')
plt.close()
'''
