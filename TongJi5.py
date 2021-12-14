from scipy import stats
from xgrads import *
import numpy as np  # 调用numpy
import xarray as xr
from math import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

air = open_CtlDataset('D:\\grads\\TongJi\\HADISST_50y.ctl')
air.attrs['pdef'] = 'None'
air.to_netcdf('D:\\grads\\TongJi\\HADISST_50y.nc')
air = xr.open_dataset('D:\\grads\\TongJi\\HADISST_50y.nc')
lonstart = 215
lonend = 307
latstart = 70
latend = 112
sst = air['sst'][:, latstart:latend, lonstart:lonend]
time = air['time'][:]
lon = air['lon'][lonstart:lonend]
lat = air['lat'][latstart:latend]
sumsst = np.zeros((len(lat), len(lon)))
sumxt = np.zeros((len(lat), len(lon)))
sst_shijian = np.zeros((len(time)))
for time_i in range(len(time)):
    a = []
    for i in range(len(lon)):
        for j in range(len(lat)):
            if float(sst[time_i, j, i]) != -999:
                a.append(float(sst[time_i, j, i]))
    sst_shijian[time_i] = sum(a) / len(a)

t = np.arange(1979, 2020, 1)
