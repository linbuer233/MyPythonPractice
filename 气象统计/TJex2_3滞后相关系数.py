from math import *

import numpy as np
import xarray as xr
from xgrads import *

############把NCEP_slp_30y_Wt转换成nc文件#############
slp = open_CtlDataset('D:\\grads\\TongJi\\NCEP_slp_30y_Wt.ctl')
slp.attrs['pdef'] = 'None'
slp.to_netcdf('D:\\grads\\TongJi\\NCEP_slp_30y_Wt.nc')
slp = xr.open_dataset('D:\\grads\\TongJi\\NCEP_slp_30y_Wt.nc')

###########把海温指数距平转成nc文件##########
air = open_CtlDataset('D:\\grads\\TongJi\\ex2\\ninosst.ctl')
air.attrs['pdef'] = 'None'
air.to_netcdf('D:\\grads\\TongJi\\ex2\\ninosst.nc')
air = xr.open_dataset('D:\\grads\\TongJi\\ex2\\ninosst.nc')

slpmin = slp['slp'][:, 12, 17]
slpmax = slp['slp'][:, 12, 33]
soi = slpmax - slpmin

#######计算海温指数滞后自相关系数#########
haiwen = air['ninosst'][:]
print(haiwen)
# 计算方差
haiwenfangcha = 0
for i in range(30):
    haiwenfangcha = haiwenfangcha + haiwen[i] ** 2
haiwenfangcha = haiwenfangcha / 30
# 自协方差
haiwenup = 0
for i in range(29):
    haiwenup = haiwenup + haiwen[i] * haiwen[i + 1]
haiwenup = haiwenup / 29
# 滞后自相关系数
rhaiwen = haiwenup / haiwenfangcha
print(rhaiwen)
########计算soi滞后自相关系数###########
# 求soi距平
temp = 0
for i in range(30):
    temp = temp + soi[i]
temp = temp / 30
soijuping = np.zeros((30))
for i in range(30):
    soijuping[i] = soi[i] - temp
# 计算方差
soifangcha = 0
for i in range(30):
    soifangcha = soifangcha + soijuping[i] ** 2
soifangcha = soifangcha / 30
# 自协方差
soiup = 0
for i in range(29):
    soiup = soiup + soijuping[i] * soijuping[i + 1]
soiup = soiup / 29
# 滞后相关系数
rsoi = soiup / soifangcha
print('\n')
print(rsoi)
print('\n')
###########两者的交叉相关系数#######
# 协方差
bothup = 0
for i in range(29):
    bothup = bothup + soijuping[i] * haiwen[i + 1]
bothup = bothup / 29
# 交叉相关系数
rsoihw = bothup / (sqrt(soifangcha) * sqrt(haiwenfangcha))
print(rsoihw)
