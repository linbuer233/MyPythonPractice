import numpy as np  # 调用numpy
from math import exp
import netCDF4 as nc
import pandas as pd

upfrist = ['air', 'hgt', 'uv']
var = ['air', 'hgt', 'u', 'v']
frist = ['1000', '925', '850', '700', '600', '500']
second = ['2021052000', '2021052006', '2021052012', '2021052018', '2021052100', '2021052106', '2021052112',
          '2021052118', '2021052200', '2021052206', '2021052212', '2021052218', '2021052300', '2021052306',
          '2021052312', '2021052318', '2021052400']

a = np.full((len(var), len(second), len(frist), 29, 45), 9.9936 * exp(-36))  # 创建一个五维数组

for k in upfrist:
    for i in frist:
        for j in second:
            filename = 'D:\\python\\tianzhen\\shixi2\\' + k + '\\' + i + '\\' + j + '.txt'
            f = open(filename, 'r', encoding='UTF-8')
            if k != 'uv':  # 读取气温，位势高度

                for bb in range(4):  # 提前读取，跳过前四行
                    b = f.readline()

                for y_i in range(28,-1,-1):
                    x_i = 0

                    for bbb in range(5):
                        List = f.readline()
                        list_start = 2  # 字符串截取起始
                        list_end = 11  # 字符串截取结束

                        for x in range(10):
                            a[upfrist.index(k), second.index(j), frist.index(i), y_i, x_i] = float(
                                List[list_start:list_end:1])
                            list_start += 10  # 跳到下一个数据的两侧
                            list_end += 10
                            x_i += 1
                            if x_i == 45:  # 第五行只有五个数据，设置提前跳出循环
                                break
            else:  # 读取uv风场
                for bb in range(3):
                    b = f.readline()
                for var_i in range(2, 4):
                    for y_i in range(28,-1,-1):
                        x_i = 0  # 数据纬向存储（按列）

                        for bbb in range(5):
                            List = f.readline()
                            list_start = 2  # 字符串截取起始
                            list_end = 11  # 字符串截取结束

                            for x in range(10):
                                a[var_i, second.index(j), frist.index(i), y_i, x_i] = float(
                                    List[list_start:list_end:1])
                                list_start += 10  # 跳到下一个数据的两侧
                                list_end += 10
                                x_i += 1
                                if x_i == 45:
                                    break
print(a[0,0,0,0,0])
##############################创建nc文件
f_w = nc.Dataset('D:\\python\\tianzhen\\shixi2\\al.nc', 'w', format('NETCDF4'))


###创建一个组容纳所有变量
all_var = f_w.createGroup('shixi')


# 定义维度
f_w.createDimension('time', 17)
f_w.createDimension('level', 6)
f_w.createDimension('lat', 29)
f_w.createDimension('lon', 45)

# 给维度设置
f_w.createVariable('time','f', 'time')
f_w.createVariable('level', np.int32, 'level')
f_w.createVariable('lat', np.float32, 'lat')
f_w.createVariable('lon', np.float32, 'lon')

# time = np.array([2021052000, 2021052006, 2021052012, 2021052018, 2021052100, 2021052106, 2021052112,
#                   2021052118, 2021052200, 2021052206, 2021052212, 2021052218, 2021052300, 2021052306,
#                   2021052312, 2021052318, 2021052400])
time=pd.date_range(start='20210520',end='20210524',periods=17)
# time= np.arange(17)
level = np.array([1000, 925, 850, 700, 600, 500])
lat = np.linspace(10, 81, 29)
lon = np.linspace(50, 160, 45)
print(len(time))

f_w.variables['time'][:] = time
f_w.variables['level'][:] = level
f_w.variables['lat'][:] = lat
f_w.variables['lon'][:] = lon
###在组里创建变量

all_var.createVariable('air', np.float32, ('time', 'level', 'lat', 'lon'))
all_var.createVariable('hgt', np.float32, ('time', 'level', 'lat', 'lon'))
all_var.createVariable('u', np.float32, ('time', 'level', 'lat', 'lon'))
all_var.createVariable('v', np.float32, ('time', 'level', 'lat', 'lon'))

###给变量设初值
var_data = np.full((17, 6, 29, 45), -99.9)
all_var.variables['air'][:] = var_data
all_var.variables['hgt'][:] = var_data
all_var.variables['u'][:] = var_data
all_var.variables['v'][:] = var_data

###给变量赋值
all_var.variables['air'][:] = a[0, :, :, :, :]

all_var.close
f_w.close()


