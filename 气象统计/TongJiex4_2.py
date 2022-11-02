from math import *

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

for i in range(len(lon)):
    for j in range(len(lat)):
        if float(st1[j, i]) > 9999:
            st1[j, i] = np.NAN
        if float(st2[j, i]) > 9999:
            st2[j, i] = np.NAN
        if float(st3[j, i]) > 9999:
            st3[j, i] = np.NAN
        if float(st4[j, i]) > 9999:
            st4[j, i] = np.NAN
        if float(st5[j, i]) > 9999:
            st5[j, i] = np.NAN

avest1 = np.nanmean(st1)
avest2 = np.nanmean(st2)
avest3 = np.nanmean(st3)
avest4 = np.nanmean(st4)
avest5 = np.nanmean(st5)
###印度太平洋海温###
lon2 = airindia['lon'][:]
lat2 = airindia['lat'][:]
st_india1 = airindia['st'][4, :, :]
st_india2 = airindia['st'][8, :, :]
st_india3 = airindia['st'][13, :, :]
st_india4 = airindia['st'][19, :, :]
st_india5 = airindia['st'][24, :, :]

for i in range(len(lon2)):
    for j in range(len(lat2)):
        if float(st_india1[j, i]) > 9999:
            st_india1[j, i] = np.NAN
        if float(st_india2[j, i]) > 9999:
            st_india2[j, i] = np.NAN
        if float(st_india3[j, i]) > 9999:
            st_india3[j, i] = np.NAN
        if float(st_india4[j, i]) > 9999:
            st_india4[j, i] = np.NAN
        if float(st_india5[j, i]) > 9999:
            st_india5[j, i] = np.NAN
avest_india1 = np.nanmean(st_india1)
avest_india2 = np.nanmean(st_india2)
avest_india3 = np.nanmean(st_india3)
avest_india4 = np.nanmean(st_india4)
avest_india5 = np.nanmean(st_india5)
###200hPa位势高度场
time = hgt['time'][:]
lonh = hgt['lon'][:]
lath = hgt['lat'][:]
hgt1 = hgt['hgt'][4, :, :]
hgt2 = hgt['hgt'][8, :, :]
hgt3 = hgt['hgt'][13, :, :]
hgt4 = hgt['hgt'][19, :, :]
hgt5 = hgt['hgt'][24, :, :]
avehgt = (hgt1 + hgt2 + hgt3 + hgt4 + hgt5) / 5
lon1, lat1 = np.meshgrid(lonh, lath)

avest = (avest1 + avest2 + avest3 + avest4 + avest5) / 5
avest_india = (avest_india1 + avest_india2 + avest_india3 + avest_india4 + avest_india5) / 5

stTP = np.array([[avest1], [avest2], [avest3], [avest4], [avest5]])
stindia = np.array([[avest_india1], [avest_india2], [avest_india3], [avest_india4], [avest_india5]])
hgtZ200 = np.array([hgt1, hgt2, hgt3, hgt4, hgt5])

###Z200和TPSST的一元回归
b = np.zeros((len(lath), len(lonh)))

for i in range(len(lonh)):
    for j in range(len(lath)):
        b[j, i] = (avest1 * hgt1[j, i] + avest2 * hgt2[j, i] + avest3 * hgt3[j, i] + avest4 * hgt4[j, i] + avest5 *
                   hgt5[j, i] - 5 * avest * avehgt[j, i]) / (
                          pow(avest1, 2) + pow(avest2, 2) + pow(avest3, 2) + pow(avest4, 2) + pow(avest5, 2) - 5 * pow(
                      avest, 2))
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b, cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\Z200andTPSST1.png')
plt.close()
###Z200和IOSST的一元回归
for i in range(len(lon1)):
    for j in range(len(lat1)):
        b[j, i] = -(avest_india1 * hgt1[j, i] + avest_india2 * hgt2[j, i] + avest_india3 * hgt3[j, i] + avest_india4 *
                    hgt4[j, i] + avest_india5 *
                    hgt5[j, i] - 5 * avest_india * avehgt[j, i]) / (
                          pow(avest_india1, 2) + pow(avest_india2, 2) + pow(avest_india3, 2) + pow(avest_india4,
                                                                                                   2) + pow(
                      avest_india5, 2) - 5 * pow(
                      avest_india, 2))
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b, cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\Z200andIOSST1.png')
plt.close()

###多元回归
stTP = np.array([[avest1], [avest2], [avest3], [avest4], [avest5]])
stindia = np.array([[avest_india1], [avest_india2], [avest_india3], [avest_india4], [avest_india5]])
hgtZ200 = np.array([hgt1, hgt2, hgt3, hgt4, hgt5])
a = np.full((5, 1), 1)
X = np.hstack((a, stTP, stindia))
X1 = np.linalg.inv((X.T).dot(X)).dot(X.T)
b = np.zeros((3, len(lat1), len(lon1)))
for i in range(len(lon1)):
    for j in range(len(lat1)):
        b[:, j, i] = X1.dot(hgtZ200[:, j, i])
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b[1, :, :], cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex42bTPSST.png')
plt.close()
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, b[2, :, :], cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex42bIOSST.png')
plt.close()

###偏相关分析方法
##1是TPSST，2是IOSST
Ry12 = np.zeros((len(lat1), len(lon1)))
Ry21 = np.zeros((len(lat1), len(lon1)))
R12y = np.zeros((len(lat1), len(lon1)))
R2y = np.zeros((len(lat1), len(lon1)))
R1y = np.zeros((len(lat1), len(lon1)))

R12 = (
              avest1 * avest_india1 + avest2 * avest_india2 + avest3 * avest_india3 + avest4 * avest_india4 + avest5 * avest_india5 - 5 * avest * avest_india) / sqrt(
    (pow(avest1, 2) + pow(avest2, 2) + pow(avest3, 2) + pow(avest4, 2) + pow(avest5, 2) - 5 * pow(avest, 2)) * (
            pow(avest_india1, 2) + pow(avest_india2, 2) + pow(avest_india3, 2) + pow(avest_india4, 2) + pow(
        avest_india5, 2) - 5 * pow(
        avest_india, 2)))
R12 = R12 * (1 + (1 - R12 * R12) / 2)
R12 = np.array(R12)
for i in range(len(lon1)):
    for j in range(len(lat1)):
        R1y[j, i] = (
                            avest1 * hgt1[j, i] + avest2 * hgt2[j, i] + avest3 * hgt3[j, i] + avest4 *
                            hgt4[j, i] + avest5 * hgt5[j, i] - 5 * avest * avehgt[j, i]) / sqrt(
            (pow(avest1, 2) + pow(avest2, 2) + pow(avest3, 2) + pow(avest4, 2) + pow(
                avest5, 2) - 5 * pow(avest, 2)) * (
                    pow(hgt1[j, i], 2) + pow(hgt2[j, i], 2) + pow(hgt3[j, i], 2) + pow(hgt4[j, i], 2) + pow(hgt5[j, i],
                                                                                                            2) - 5 * pow(
                avehgt[j, i], 2)))
        R2y[j, i] = (
                            avest_india1 * hgt1[j, i] + avest_india2 * hgt2[j, i] + avest_india3 * hgt3[
                        j, i] + avest_india4 *
                            hgt4[j, i] + avest_india5 * hgt5[j, i] - 5 * avest_india * avehgt[j, i]) / sqrt(
            (pow(avest_india1, 2) + pow(avest_india2, 2) + pow(avest_india3, 2) + pow(avest_india4, 2) + pow(
                avest_india5, 2) - 5 * pow(avest_india, 2)) * (
                    pow(hgt1[j, i], 2) + pow(hgt2[j, i], 2) + pow(hgt3[j, i], 2) + pow(hgt4[j, i], 2) + pow(hgt5[j, i],
                                                                                                            2) - 5 * pow(
                avehgt[j, i], 2)))
        R1y[j, i] = R1y[j, i] * (1 + (1 - pow(R1y[j, i], 2)) / (2 * (5 - 4)))
        R2y[j, i] = R2y[j, i] * (1 + (1 - pow(R2y[j, i], 2)) / (2 * (5 - 4)))
        Ry12[j, i] = (R1y[j, i] - R12 * R2y[j, i]) / (sqrt(1 - pow(R2y[j, i], 2)) * sqrt(1 - pow(R12, 2)))
        Ry21[j, i] = (R2y[j, i] - R12 * R1y[j, i]) / (sqrt(1 - pow(R1y[j, i], 2)) * sqrt(1 - pow(R12, 2)))
        R12y[j, i] = (R12 - R1y[j, i] * R2y[j, i]) / sqrt((1 - pow(R1y[j, i], 2)) * (1 - pow(R2y[j, i], 2)))
        if Ry12[j, i] >= 1 or Ry12[j, i] <= -1:
            Ry12[j, i] = 0
        if Ry21[j, i] >= 1 or Ry21[j, i] <= -1:
            Ry21[j, i] = 0
        if R12y[j, i] >= 1 or R12y[j, i] <= -1:
            R12y[j, i] = 0
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, Ry12, cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex43RTPSST.png')
plt.close()
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, Ry21, cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex43RIOSST.png')
plt.close()
ax, fig = createmap()
colorbar = ax.contourf(lon1, lat1, R12y, cmap='bwr', transform=ccrs.PlateCarree())
plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
plt.savefig(r'D:\grads\TongJi\ex4\ex43R12y.png')
plt.close()
