import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter
from metpy.units import units

#################################################################################################
all_vars = xr.open_dataset('D:\\python\\tianzhen\\shixi2\\all.nc')
lons = all_vars.coords['lon'][:]
lats = all_vars['lat'][:]
levels = all_vars.coords['level'][:]
lon, lat = np.meshgrid(lons, lats)
lon = lon * units.degrees_east
lon, level = np.meshgrid(lons, levels)
# level=level*units.hPa
####赋上单位,度数
lons = lons * units.degrees_east
lats = lats * units.degrees_north
dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)  ###后面散度计算需要

uwind_levels = all_vars['u'][0, :, :, :]
vwind_levels = all_vars['v'][0, :, :, :]
####赋上单位，m/s
uwind_levels = uwind_levels * (units.m / units.s)
vwind_levels = vwind_levels * (units.m / units.s)
###################################################################################################
Pcha = [75, 75, 150, 100, 100]
div = np.zeros((6, 29, 45))
W_speed = np.zeros((6, 29, 45))
W_speed_Xiu = np.zeros((6, 29, 45))
for h_i in range(6):
    # 计算散度
    div[h_i, :, :] = mpcalc.divergence(uwind_levels[h_i, :, :], vwind_levels[h_i, :, :], dx=dx[:, :], dy=dy[:, :])
for h_i in range(1, 6):
    W_speed[h_i, :, :] = W_speed[h_i - 1, :, :] + 0.5 * (div[h_i, :, :] - div[h_i - 1, :, :]) * Pcha[h_i - 1]
for h_i in range(5):
    W_speed_Xiu[h_i, :, :] = W_speed[h_i, :, :] - h_i * (h_i + 1) / (7 * 6) * (W_speed[5, :, :] - W_speed_Xiu[5, :, :])
#############################################################绘图##################################3
fig = plt.figure()
ax = fig.subplots(1, 1)
plt.contourf(lon, level, W_speed_Xiu[:, 11, :])
plt.colorbar()
#####横坐标显示经度
lon_formatter = LongitudeFormatter(zero_direction_label=False)
ax.xaxis.set_major_formatter(lon_formatter)
####纵坐标格式显示
ax.invert_yaxis()
ax.set_yscale('symlog')
plt.yticks([1000, 900, 800, 700, 600, 500], ["1000", "900", "800", "700", "600", "500"])
ax.set_ylabel('hPa')
plt.show()
