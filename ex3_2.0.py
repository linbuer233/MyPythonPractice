'''
实习三：已知2021年7月17日00时-22日18时北半球的风场(u,v)、高度场(h)、温度场和相对湿度每日四次的等压面资料，
请利用相关资料求出（东经50-160，北纬10-80）区域内
（1）垂直速度。
（2）进行散度和垂直速度的订正（第二种修正方案，其余修正方案可自行选择尝试）。
当然环流形势分析也是需要的。
2021/11/7
'''
########需要用到的模块
import os
import numpy as np  # 调用numpy
import pandas as pd
import xarray as xr
from math import *
import metpy.calc as mpcalc
from metpy.units import units
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
plt.rcParams['axes.unicode_minus'] = False  ###用来正常显示负号


##地图创建函数
def createmap():
    ###################################地图设置##########################
    fig = plt.figure(figsize=(9, 6), dpi=150)  # 画布大小
    ax = fig.subplots(1, 1,
                      subplot_kw={'projection': ccrs.LambertConformal(central_longitude=105, central_latitude=30)})
    ax.add_feature(cfeature.COASTLINE.with_scale('110m'))
    ax.add_geometries(Reader('D:\\maplist\\China_province\\bou2_4l.shp').geometries(), ccrs.PlateCarree(),
                      facecolor='none', edgecolor='gray', linewidth=0.8)  ###添加省界
    Lam = ax.gridlines(draw_labels=True, linestyle=':', linewidth=0.3, x_inline=False, y_inline=False, color='k')
    Lam.top_labels = True  ##关闭上面的经纬度标签
    Lam.right_labels = False
    Lam.xformatter = LONGITUDE_FORMATTER
    Lam.yformatter = LATITUDE_FORMATTER
    Lam.xlocator = mticker.FixedLocator(np.arange(50, 160, 10))
    Lam.ylocator = mticker.FixedLocator(np.arange(10, 80, 10))
    Lam.xlabel_style = {'size': 4}
    Lam.ylabel_style = {'size': 4}

    # 经纬度格式，把0经度设置不加E和W
    # lon_formatter = LongitudeFormatter(zero_direction_label=False)
    # lat_formatter = LatitudeFormatter()
    # ax.xaxis.set_major_formatter(lon_formatter)
    # ax.yaxis.set_major_formatter(lat_formatter)
    ax.set_extent([50, 160, 10, 80], ccrs.PlateCarree())  ## 调整图片大小在画布中

    return ax, fig


ax, fig = createmap()
plt.show()
######################################################################

wenjian = ['hgt', 't', 'uv', 'rh']
NY = 37
NX = 73
#####################################################创建数组#############################################################
for var_i in wenjian:
    wenjian_path = 'D:\\python\\tianzhen\\shixi3_4\\data\\' + var_i
    level = []  #####设置一个空列表，方便后面获取每个要素高度的层数，方便之后创建数组
    ##在各个要素文件下遍历，获取创建数组所需的维度大小，除了格点数
    for root, dirs, files in os.walk(wenjian_path):
        ##获取高度层数
        #####让dirs里高度文件夹按数值大小排序，以防止数据存放到数组里的顺序错误
        a = np.zeros(len(dirs))
        for i in dirs:
            a[dirs.index(i)] = int(i)
        b = list(np.sort(a))  #####排序，从小到大
        for i in b:
            dirs[b.index(i)] = str(int(i))
        level.append(dirs)
        if not var_i == 'rh':
            level_other = level
        ##获取时间维度，同时方便后续给画出的图命名
        for d in dirs:
            wenjian_timename = os.listdir(os.path.join(root, d))
            for i in wenjian_timename:
                wenjian_timename[wenjian_timename.index(i)] = i[:-4]
    if var_i == 'rh':
        rh = np.full((len(level) - 1, len(wenjian_timename), NY, NX), 0.000)
    else:
        hgt_t_uv = np.full((4, len(level) - 1, len(wenjian_timename), NY, NX), 0.000)

########################################################读取数据，os文件遍历################################################
for var_i in wenjian:
    wenjian_path = 'D:\\python\\tianzhen\\shixi3_4\\data\\' + var_i
    #####设置一个空列表，当作数据存放的中继点
    hgt_t_data = []
    uv_data = []
    rh_data = []
    for root, dirs, files in os.walk(wenjian_path):
        #####让dirs里高度文件夹按数值大小排序，以防止数据存放到数组里的顺序错误
        a = np.zeros(len(dirs))
        for i in dirs:
            a[dirs.index(i)] = int(i)
        b = list(np.sort(a))  #####排序，从小到大
        for i in b:
            dirs[b.index(i)] = str(int(i))

        if var_i == 'uv':
            for f in files:
                data = pd.read_csv(os.path.join(root, f), skiprows=3, header=None, sep='\s+')
                zhongJian = data.values.reshape(2, NY, 80)
                zhongJian = np.delete(zhongJian, list(range(NX, 80)), axis=2)  ####去掉末尾的Nan值
                uv_data.append(zhongJian)  #
        if var_i == 'rh':
            for f in files:
                data = pd.read_csv(os.path.join(root, f), skiprows=4, header=None, sep='\s+')
                zhongJian = data.values.reshape(NY, 80)
                zhongJian = np.delete(zhongJian, list(range(NX, 80)), axis=1)  ####去掉末尾的Nan值
                rh_data.append(zhongJian)  #
        if var_i == 'hgt' or var_i == 't':
            for f in files:
                data = pd.read_csv(os.path.join(root, f), skiprows=4, header=None, sep='\s+')
                zhongJian = data.values.reshape(NY, 80)
                zhongJian = np.delete(zhongJian, list(range(NX, 80)), axis=1)  ####去掉末尾的Nan值
                hgt_t_data.append(zhongJian)  #
    if var_i == 'uv':
        uv_data_array = np.array(uv_data)
        uv_data_array = uv_data_array.reshape(hgt_t_uv.shape[1], hgt_t_uv.shape[2], 2, NY, NX)
        uv_data_array = uv_data_array[::-1, :, :, ::-1, :]  ###反转高度轴，和维度轴
        hgt_t_uv[2, :, :, :, :] = uv_data_array[:, :, 0, :, :]
        hgt_t_uv[3, :, :, :, :] = uv_data_array[:, :, 1, :, :]
    if var_i == 'rh':
        rh_data_array = np.array(rh_data)
        rh_data_array = rh_data_array.reshape(rh.shape[0], rh.shape[1], NY, NX)
        rh_data_array = rh_data_array[::-1, :, ::-1, :]  ###反转高度轴和维度轴
        rh = rh_data_array
    if var_i == 'hgt' or var_i == 't':
        hgt_t_data_array = np.array(hgt_t_data)
        hgt_t_data_array = hgt_t_data_array.reshape(hgt_t_uv.shape[1], hgt_t_uv.shape[2], NY, NX)
        hgt_t_data_array = hgt_t_data_array[::-1, :, ::-1, :]  ###反转高度轴和维度轴
        hgt_t_uv[wenjian.index(var_i), :, :, :, :] = hgt_t_data_array

###################################################存放到nc文件中#########################################################
starttime = wenjian_timename[0]
starttime = starttime[:-2]
endtime = wenjian_timename[-1]
endtime = endtime[:-2]
time = pd.date_range(start=starttime, end=endtime, periods=len(wenjian_timename))
levels = level_other[0]
levels = levels[::-1]  ##翻转
for h in levels:
    levels[levels.index(h)] = float(h)
lat = np.arange(0, 91, 2.5)
lon = np.arange(0, 181, 2.5)

hgt = hgt_t_uv[0, :, :, :, :]
t = hgt_t_uv[1, :, :, :, :]
u = hgt_t_uv[2, :, :, :, :]
v = hgt_t_uv[3, :, :, :, :]

ds_hgt_t_uv = xr.Dataset({
    'hgt': (['level', 'time', 'lat', 'lon'], hgt),
    't': (['level', 'time', 'lat', 'lon'], t),
    'u': (['level', 'time', 'lat', 'lon'], u),
    'v': (['level', 'time', 'lat', 'lon'], v)
},
    coords={'lon': (['lon'], lon),
            'lat': (['lat'], lat),
            'time': (['time'], time),
            'level': (['level'], levels)
            })
ds_hgt_t_uv.to_netcdf('D:\\python\\tianzhen\\shixi3_4\\ds_hgt_t_uv.nc')

levels = level[0]
levels = levels[::-1]  ###翻转
for h in levels:
    levels[levels.index(h)] = float(h)
ds_rh = xr.Dataset({'rh': (['level', 'time', 'lat', 'lon'], rh)},
                   coords={'lon': (['lon'], lon),
                           'lat': (['lat'], lat),
                           'time': (['time'], time),
                           'level': (['level'], levels)
                           })
ds_rh.to_netcdf('D:\\python\\tianzhen\\shixi3_4\\ds_rh.nc')
########################################################################################################################

##读取数据
ds = xr.open_dataset('D:\\python\\tianzhen\\shixi3_4\\ds_hgt_t_uv.nc')
lons = ds['lon'][:]
lats = ds['lat'][:]
levels = ds['level'][:]
time = ds['time'][:]
uwind = ds['u'][:, :, :, :]  ##高度|时间|维度|经度
vwind = ds['v'][:, :, :, :]  ##高度|时间|维度|经度
hgt = ds['hgt'][:, :, :, :]  ##高度|时间|维度|经度
Temp = ds['t'][:, :, :, :]  ##高度|时间|维度|经度
##给个单位,防止metpy计算报错
lons = lons * units.degrees_east
lats = lats * units.degrees_north
uwind = uwind * (units.m / units.s)
vwind = vwind * (units.m / units.s)
dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)  ###后面散度计算需要
lon, lat = np.meshgrid(lons, lats)  ##画平面图用
lon, level = np.meshgrid(lons, levels)  ##画剖面图用
lat, level = np.meshgrid(lats, levels)  ##画剖面图用

###求垂直速度
level_uv = levels.data
Pcha = []  ##相邻两层的气压差
for i in range(len(level_uv) - 1):
    Pcha.append(float(level_uv[i + 1]) - float(level_uv[i]))
Pcha = Pcha * 100  ###翻转，从地面相邻两层开始，并转成Pa
div = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
W_speed = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
W_speed_Xiu = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv)):
        ##计算散度 1/s
        div[h_i, time_i:, :] = mpcalc.divergence(uwind[h_i, time_i, :, :], vwind[h_i, time_i, :, :], dx=dx[:, :],
                                                 dy=dy[:, :])
##计算垂直速度  单位Pa/s
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(1, len(level_uv)):
        W_speed[h_i, time_i, :, :] = W_speed[h_i - 1, time_i, :, :] + 0.5 * (
                div[h_i, time_i, :, :] - div[h_i - 1, time_i, :, :]) * Pcha[h_i - 1]  ##公式
##修正方案二修正垂直速度 单位Pa/s
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv) - 1):
        W_speed_Xiu[h_i, time_i, :, :] = W_speed[h_i, time_i, :, :] - h_i * (h_i + 1) / (
                (len(level_uv) + 1) * len(level_uv)) * W_speed[len(level_uv) - 1, time_i, :, :]
##计算涡度
wodu = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv)):
        wodu[h_i, time_i, :, :] = mpcalc.vorticity(uwind[h_i, time_i, :, :], vwind[h_i, time_i, :, :], dx=dx[:, :],
                                                   dy=dy[:, :])

###计算假相当位温
##设定一些常量
Rd = 287  # J/(K*kg)
L = 2.5 * 10 ** 6  # J/kg
Cp = 1004  # J/(K*kg)
a = 17.2693882
b = 35.86
##读取rh
RH = xr.open_dataset(r'D:\python\tianzhen\shixi3_4\ds_rh.nc')
Theta_rh = RH['rh'][:, :, :, :]  ###高度|时间|维度|经度
rh_level = RH['level'][:]
rh_P = []
for i in rh_level:
    rh_P.append(float(i))
rh_time = ['time'][:]
#
Tempd = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))  ##露点温度
Thetase = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))  ##假相当位温

for time_i in range(len(rh_time)):
    for h_i in range(len(rh_level)):
        for x in range(rh.shape[3]):
            for y in range(rh.shape[2]):
                es = 6.1078 * np.exp(a * (Temp[h_i, time_i, y, x]) / (Temp[h_i, time_i, y, x] + 273.16 - b))
                e = Theta_rh[h_i, time_i, y, x] * es
                Tempd0 = Temp[h_i, time_i, y, x] + 273.16
                while True:
                    e0 = 6.1078 * np.exp(a * (Tempd0 - 273.16) / (Tempd0 - b))
                    if e < e0:
                        Tempd0 = Tempd0 - 0.1  #########
                    else:
                        Tempd[h_i, time_i, y, x] = Tempd0
                        break
for time_i in range(len(rh_time)):
    for h_i in range(len(rh_level)):
        es = 6.1078 * np.exp(a * (Temp[h_i, time_i, :, :]) / (Temp[h_i, time_i, :, :] + 273.16 - b))
        e = Theta_rh[h_i, time_i, :, :] * es
        q = 622 * e / (rh_P[h_i] - 0.378 * e)  # g/kg
        Thetase[h_i, time_i, :, :] = (Temp[h_i, time_i, :, :] + 273.16) * np.exp(
            Rd / Cp * np.log(1000 / (rh_P[h_i] - e)) + L * q / (Cp * Tempd[h_i, time_i, :, :]) + q / 0.622 * np.log(
                (Temp[h_i, time_i, :, :] + 273.16) / Tempd[h_i, time_i, :, :]))

########################################################绘图部分#####################################################
##各个高度，各个时次的涡度——等高线
'''
wodu_level = []
for i in levels.data:
    wodu_level.append(str(i))
for time_i in range(len(time)):
    for h_i in range(len(wodu_level)):
        ax, fig = createmap()

        hgt_jiange = np.arange(-1000, 2000, 4)
        dengHGTlines = ax.contour(lons, lats, hgt[h_i, time_i, :, :], levels=hgt_jiange, colors='b',
                                  linewidths=0.8, linestyles='-', extend='both',
                                  transform=ccrs.PlateCarree())
        plt.clabel(dengHGTlines, inline=True, fontsize=8, fmt='%.0f')

        colorbar = ax.contourf(lons, lats, wodu[h_i, time_i, :, :], transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        titlename = wodu_level[h_i] + '_' + wenjian_timename[time_i] + '时涡度—等高场'
        ax.set_title(titlename)
        ax.grid()
        picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\涡度-位势场\\ ' + wodu_level[h_i]
        if not os.path.exists(picturepath):
            os.makedirs(picturepath)
        picturename = picturepath + '\\' + titlename + '.png'
        plt.savefig(picturename)
        plt.close()
'''
print(Thetase)