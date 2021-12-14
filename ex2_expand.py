import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


###############################合成多个nc文件
# a=xr.open_mfdataset('D:\\python\\tianzhen\\1980-2010airTlevel\\air.*.nc')
# a.to_netcdf('D:\\python\\tianzhen\\1980-2010airTlevel\\1.nc')
# a=xr.open_mfdataset('D:\\python\\tianzhen\\1980-2010airsurface\\air.sig995.*.nc')
# a.to_netcdf('D:\\python\\tianzhen\\1980-2010airsurface\\2.nc')
###############################

air_baiyin = xr.open_dataset('D:\\python\\tianzhen\\shixi2\\all.nc')
air_global_levels = xr.open_dataset('D:\\python\\tianzhen\\1980-2010airTlevel\\air.mon.mean.nc')
# air_global_surface = xr.open_dataset('D:\\python\\tianzhen\\1980-2010airsurface\\air.mon.meansurface.nc')
a=0
levels = [0, 2, 3]
temp = np.full((3, 1), 0.00)
ave_levels = np.full((3, 1), 0.00)
for h in levels:
    time = 389
    for t_i in range(31):

        a+= air_global_levels['air'][time, h, 22, 42]
        time=time+12
    temp[levels.index(h),:]=a
    ave_levels[levels.index(h), :] = temp[levels.index(h), :] / 31
# tem = np.full((1), 0)
# ave = np.full((1), 0)
# time = 4
# for t_i in range(31):
#     if time >= 745:
#         break
#     tem = air_global_surface['air'][time, 22, 42] + air_global_surface['air'][time + 12, 22, 42]
# ave = tem / 31

air1=np.full((17),0)
baiyintime = air_baiyin['time'][:]
for  h in levels:
   for t_i in range(17):
        air1[t_i] = air_baiyin['air'][t_i, levels.index(h), 10, 22] - ave_levels[levels.index(h), 0]

   plt.plot(baiyintime,air1)
   plt.gcf().autofmt_xdate()
   plt.savefig('D:\\python\\tianzhen\\'+str(levels.index(h)))
   plt.close()


