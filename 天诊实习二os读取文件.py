'''
天诊实习2，利用os遍历，读取文件，并存到一个nc文件中
'''
import os
import pandas as pd
import numpy as np
import xarray as xr

varname = ['air', 'hgt', 'uv']
allvars = np.full((4, 6, 17, 29, 45), 0.000)
for var_i in varname:
    aaa = []  ###设置一个空列表，方便后面读取文件追加
    bbb = []
    file = 'D:\\python\\tianzhen\\shixi2\\data\\' + var_i
    for root, dirs, files in os.walk(file):  #####当前路径，路径下的子文件夹，文件
        a = np.zeros(len(dirs))  #####让dirs里高度文件夹按数值大小排序
        for i in dirs:
            a[dirs.index(i)] = int(i)
        b = list(np.sort(a))    #####排序，从小到大
        for i in b:
            dirs[b.index(i)] = str(int(i))
        ###遍历文件  os.path.join(a,b)是把a和b 合为一个路径
        if not var_i == 'uv':
            for f in files:
                data_air = pd.read_csv(os.path.join(root, f), skiprows=4, header=None, sep='\s+')
                hh = data_air.values.reshape(29, 50)
                hh = np.delete(hh, list(range(45, 50)), axis=1)  ####去掉末尾的nan值
                aaa.append(hh)                          ####列表追加
        else:
            for f in files:
                data_air = pd.read_csv(os.path.join(root, f), skiprows=3, header=None, sep='\s+')
                hh = data_air.values.reshape(2, 29, 50)
                hh = np.delete(hh, list(range(45, 50)), axis=2)  ####去掉末尾的nan值
                bbb.append(hh)                         ####列表追加
    if var_i == 'uv':
        bbb_array = np.array(bbb)                      #####把列表bbb转化成数组
        bbb_array = bbb_array.reshape(6, 17, 2, 29, 45)
        bbb_array = bbb_array[::-1, :, :, ::-1, :]#####反转y轴和高度轴
    else:
        aaa_array = np.array(aaa)                #####把列表bbb转化成数组
        aaa_array = aaa_array.reshape(6, 17, 29, 45)
        aaa_array = aaa_array[::-1, :, ::-1, :]#####反转y轴和高度轴
        allvars[varname.index(var_i), :, :, :, :] = aaa_array
allvars[2, :, :, :, :] = bbb_array[:, :, 0, :, :]
allvars[3, :, :, :, :] = bbb_array[:, :, 1, :, :]
#######################################存放到nc文件中######################
time = pd.date_range(start='20210520', end='20210524', periods=17)
level = np.array([1000, 925, 850, 700, 600, 500], dtype=float)
lat = np.arange(10, 81, 2.5)
lon = np.arange(50, 161, 2.5)

air = allvars[0, :, :, :, :]
hgt = allvars[1, :, :, :, :]
u = allvars[2, :, :, :, :]
v = allvars[3, :, :, :, :]
all_vars = xr.Dataset({'air': (['level', 'time', 'lat', 'lon'], air),
                       'hgt': (['level', 'time', 'lat', 'lon'], hgt),
                       'u': (['level', 'time', 'lat', 'lon'], u),
                       'v': (['level', 'time', 'lat', 'lon'], v)},

                      coords={'lon': (['lon'], lon),
                              'lat': (['lat'], lat),
                              'time': (['time'], time),
                              'level': (['level'], level)
                              })
all_vars.to_netcdf('D:\\python\\tianzhen\\shixi2\\data\\vars.nc')
