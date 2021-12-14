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
import metpy.constants as constants
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']  ###防止无法显示中文并设置黑体
plt.rcParams['axes.unicode_minus'] = False  ###用来正常显示负号


##时间处理,加个八小时
def shijianchuli(img_name):
    bigmonth = ['01', '03', '04', '05', '07', '08', '10', '12']
    img_name_year = img_name[:4]
    img_name_month = img_name[4:6]
    img_name_day = img_name[6:8]
    img_name_hour = str(int(img_name[8:10]) + 108)  ###转换成北京时间，并且为了小时显示00这样的格式，加了108，后面再截取

    ####对日期的处理，有些加了八小时变成北京时间之后，日期会发生改变，下面就是对日期在闰年、非闰年，大小月等情况时的处理
    if int(img_name_hour) > 124:
        img_name_day = str(int(img_name_day) + 101)
        img_name_day = img_name_day[1:3]
        img_name_hour = str(int(img_name_hour) - 24)
        img_name_hour = img_name_hour[1:3]
        if int(img_name_year) % 4 == 0 and int(img_name_year) % 100 != 0:  ####闰年的判定
            if img_name_month == '02':
                if int(img_name_day) > 29:
                    img_name_day = '01'
            if img_name_month in bigmonth:
                if int(img_name_day) > 31:
                    img_name_month = str(int(img_name_month) + 1)
                    img_name_day = '01'
            else:
                if int(img_name_day) > 30:
                    img_name_month = str(int(img_name_month) + 1)
                    img_name_day = '01'
        else:
            if img_name_month == '02':
                if int(img_name_day) > 28:
                    img_name_day = '01'
            if img_name_month in bigmonth:
                if int(img_name_day) > 31:
                    img_name_month = str(int(img_name_month) + 1)
                    img_name_day = '01'
            else:
                if int(img_name_day) > 30:
                    img_name_month = str(int(img_name_month) + 1)
                    img_name_day = '01'
    else:
        img_name_hour = img_name_hour[1:3]
    daytime = img_name_year + '_' + img_name_month + '_' + img_name_day + '_' + img_name_hour
    return daytime


##地图创建函数
def createmap():
    ###################################地图设置##########################
    fig = plt.figure(figsize=(9, 6), dpi=150)  # 画布大小
    ax = fig.subplots(1, 1,
                      subplot_kw={'projection': ccrs.LambertConformal(central_longitude=105, central_latitude=30)})
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_geometries(Reader('D:\\maplist\\China_province\\bou2_4l.shp').geometries(), ccrs.PlateCarree(),
                      facecolor='none', edgecolor='gray', linewidth=0.8)  ###添加省界
    ax.add_geometries(Reader('D:\\maplist\\zhengzhou\\郑州市.shp').geometries(), ccrs.PlateCarree(),
                      facecolor='none', edgecolor='r', linewidth=0.8)  ###添加郑州市界
    Lam = ax.gridlines(draw_labels=True, linestyle=':', linewidth=0.3, x_inline=False, y_inline=False, color='k')
    Lam.top_labels = True  ##打开上面的经纬度标签
    Lam.right_labels = False  ###关闭右边
    Lam.xformatter = LONGITUDE_FORMATTER
    Lam.yformatter = LATITUDE_FORMATTER
    Lam.xlocator = mticker.FixedLocator(np.arange(0, 180, 10))
    Lam.ylocator = mticker.FixedLocator(np.arange(10, 80, 10))
    Lam.xlabel_style = {'size': 7}
    Lam.ylabel_style = {'size': 7}
    ax.set_extent([60, 135, 10, 70], ccrs.PlateCarree())  ## 调整图片大小在画布中

    return ax, fig

ax,fig=createmap()
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
lon1, level1 = np.meshgrid(lons, levels)  ##画维向剖面图用
lat2, level2 = np.meshgrid(lats, levels)  ##画经向剖面图用

###求垂直速度
level_uv = list(levels.data)
Pcha = []  ##相邻两层的气压差
for i in range(len(level_uv) - 1):
    Pcha.append((level_uv[i + 1] - level_uv[i]) * (-100))  ###翻转，从地面相邻两层开始，并转成Pa
div = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
div_Xiu = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
W_speed = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
W_speed_Xiu = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv)):
        ##计算散度 1/s
        div[h_i, time_i:, :] = mpcalc.divergence(uwind[h_i, time_i, :, :], vwind[h_i, time_i, :, :], dx=dx[:, :],
                                                 dy=dy[:, :])  # metpy公式
##计算垂直速度  单位Pa/s
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(1, len(level_uv)):
        W_speed[h_i, time_i, :, :] = W_speed[h_i - 1, time_i, :, :] + 0.5 * (
                div[h_i, time_i, :, :] + div[h_i - 1, time_i, :, :]) * Pcha[h_i - 1]  ##公式
##修正方案二修正垂直速度,散度 单位Pa/s
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv) - 1):
        W_speed_Xiu[h_i, time_i, :, :] = W_speed[h_i, time_i, :, :] - h_i * (h_i + 1) / (
                (len(level_uv) + 1) * len(level_uv)) * W_speed[len(level_uv) - 1, time_i, :, :]
        div_Xiu[h_i, time_i, :, :] = div[h_i, time_i, :, :] - h_i / (
                0.5 * (len(level_uv) - 1) * len(level_uv) * Pcha[h_i]) * W_speed[len(level_uv) - 1, time_i, :, :]  # 公式
##计算涡度
wodu = np.zeros((len(level_uv), hgt_t_uv.shape[2], NY, NX))
for time_i in range(hgt_t_uv.shape[2]):
    for h_i in range(len(level_uv)):
        wodu[h_i, time_i, :, :] = mpcalc.vorticity(uwind[h_i, time_i, :, :], vwind[h_i, time_i, :, :], dx=dx[:, :],
                                                   dy=dy[:, :])  # metpy公式

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
rh_time = RH['time'][:]
lon_rh1, level_rh1 = np.meshgrid(lons, rh_level)  ##画经向剖面图用
lat_rh2, level_rh2 = np.meshgrid(lats, rh_level)  ##画纬向剖面图用
'''
###假相当位温计算
Tempd = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))  ##露点温度
Thetase = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))  ##假相当位温
es = np.zeros((rh.shape[2], rh.shape[3]))
e0 = np.zeros((rh.shape[2], rh.shape[3]))
e = np.zeros((rh.shape[2], rh.shape[3]))
Tempd0 = np.zeros((rh.shape[2], rh.shape[3]))
q = np.zeros((rh.shape[2], rh.shape[3]))
######################################运行耗时过长###################################################################
for h_i in range(len(rh_level)):
    for time_i in range(len(rh_time)):
        es[:, :] = 6.1078 * np.exp(a * (Temp[h_i, time_i, :, :]) / (Temp[h_i, time_i, :, :] + 273.16 - b))
        e[:, :] = Theta_rh[h_i, time_i, :, :] * es / 100
        q[:, :] = 0.622 * e[:, :] / (rh_P[h_i] - 0.378 * e[:, :])  # g/g
        Tempd0[:, :] = Temp[h_i, time_i, :, :] + 273.16
        for y in range(rh.shape[2]):
            for x in range(rh.shape[3]):
                while True:
                    e0[y, x] = 6.1078 * exp(a * (Tempd0[y, x] - 273.16) / (Tempd0[y, x] - b))
                    if e[y, x] < e0[y, x]:
                        Tempd0[y, x] = Tempd0[y, x] - 1  #########
                    else:
                        Tempd[h_i, time_i, y, x] = Tempd0[y, x]
                        break
                Thetase[h_i, time_i, y, x] = (Temp[h_i, time_i, y, x] + 273.16) * exp(
                    Rd / Cp * log(1000 / (rh_P[h_i] - e[y, x])) + L * q[y, x] / (
                            Cp * Tempd[h_i, time_i, y, x]) + q[y, x] / 0.622 * log(
                        (Temp[h_i, time_i, y, x] + 273.16) / Tempd[h_i, time_i, y, x]))
'''
'''
########################################################绘图部分#####################################################
##各个高度，各个时次的涡度——等高线

wodu_level = []
for i in levels.data:
    wodu_level.append(str(i))
hgt_jiange = np.arange(-1000, 2000, 4)
for h_i in range(len(wodu_level)):
    for time_i in range(len(time)):
        ax, fig = createmap()
        dengHGTlines = ax.contour(lons, lats, hgt[h_i, time_i, :, :], levels=hgt_jiange, colors='b',
                                  linewidths=0.8, linestyles='-', extend='both',
                                  transform=ccrs.PlateCarree())
        plt.clabel(dengHGTlines, inline=True, fontsize=8, fmt='%.0f')

        colorbar = ax.contourf(lons, lats, wodu[h_i, time_i, :, :], transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        titlename = wodu_level[h_i] + '_' + shijianchuli(wenjian_timename[time_i]) + '时涡度—等高场'
        ax.set_title(titlename)
        ax.grid()
        plt.tight_layout()###让图填充整个画布
        picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\涡度-位势场\\' + wodu_level[h_i]
        if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
            os.makedirs(picturepath)
        picturename = picturepath + '\\' + titlename + '.png'
        plt.savefig(picturename)
        plt.close()

###假相当位温与垂直速度修正的剖面图 各个时次，经向剖面图112.5E
Thetase_jiange = np.arange(-1000, 1500, 8)
for time_i in range(len(rh_time)):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1)
    dengThetaselines = ax.contour(lat_rh2, level_rh2, Thetase[:, time_i, :, 45], Thetase_jiange, colors='k',
                                  linewidths=0.8, linestyles='-', extend='both')
    plt.clabel(dengThetaselines, inline=True, fontsize=8, fmt='%.0f')
    colorbar = ax.contourf(lat_rh2, level_rh2, W_speed_Xiu[:len(rh_level), time_i, :, 45],
                           cmap='Spectral')
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    #####横坐标显示维度
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lat_formatter)
    ####纵坐标格式显示
    ax.invert_yaxis()
    ax.set_yscale('symlog')
    ##暴力显示
    plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300], ["1000", "900", "800", "700", "600", "500", "400", "300"])
    ax.set_ylabel('hPa')
    titlename = shijianchuli(wenjian_timename[time_i]) + '时假相当位温垂直速度经向剖面图'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\假相当位温_垂直速度经向剖面图\\'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()
###假相当位温与垂直速度修正的剖面图 各个时次，维向剖面图35N
for time_i in range(len(rh_time)):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1)
    dengThetaselines = ax.contour(lon_rh1, level_rh1, Thetase[:, time_i, 14, :], Thetase_jiange, colors='k',
                                  linewidths=0.8, linestyles='-', extend='both')
    plt.clabel(dengThetaselines, inline=True, fontsize=8, fmt='%.0f')
    colorbar = ax.contourf(lon_rh1, level_rh1, W_speed_Xiu[:len(rh_level), time_i, 14, :],
                           cmap='Spectral')
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    #####横坐标显示经度
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    ax.xaxis.set_major_formatter(lon_formatter)
    ####纵坐标格式显示
    ax.invert_yaxis()
    ax.set_yscale('symlog')
    ##暴力显示
    plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300], ["1000", "900", "800", "700", "600", "500", "400", "300"])
    ax.set_ylabel('hPa')

    titlename = shijianchuli(wenjian_timename[time_i]) + '时假相当位温垂直速度纬向剖面图'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\假相当位温_垂直速度纬向剖面'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()
'''
'''
###环流形势500hPa，850hPa，地面
huangliu_Jiange = np.arange(-1000, 1500, 4)
huanliugaodu = [1000, 850, 500]
for h_i in huanliugaodu:
    for time_i in range(len(time)):
        ax, fig = createmap()
        dengHGTlines = ax.contour(lons, lats, hgt[level_uv.index(h_i), time_i, :, :], levels=huangliu_Jiange,
                                  colors='b', linewidths=0.8,
                                  linestyles='-', extend='both',
                                  transform=ccrs.PlateCarree())
        plt.clabel(dengHGTlines, inline=True, fontsize=8, fmt='%.0f')
        dengTemplines = ax.contour(lons, lats, Temp[level_uv.index(h_i), time_i, :, :], levels=huangliu_Jiange,
                                   colors='r', linewidths=0.8,
                                   linestyles='-', extend='both',
                                   transform=ccrs.PlateCarree())
        plt.clabel(dengTemplines, inline=True, fontsize=8, fmt='%.0f')
        wind_slice = (slice(None, None, 2), slice(None, None, 2))  ####调风羽的密度
        uwind_huanliu = np.array(uwind[level_uv.index(h_i), time_i, :, :])
        vwind_huanliu = np.array(vwind[level_uv.index(h_i), time_i, :, :])
        plt.barbs(lon[wind_slice], lat[wind_slice], uwind_huanliu[wind_slice], vwind_huanliu[wind_slice],
                  pivot='middle', length=4, barb_increments=dict(half=2, full=4, flag=20),
                  color='black', transform=ccrs.PlateCarree())
        #########[x,y,u,v]  这四个都要 ndarray 形式
        titlename = str(h_i) + '_' + shijianchuli(wenjian_timename[time_i]) + '时环流形势'
        ax.set_title(titlename)
        ax.grid()
        plt.tight_layout()  ###让图填充整个画布
        picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\环流形势\\' + str(h_i)
        if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
            os.makedirs(picturepath)
        picturename = picturepath + '\\' + titlename + '.png'
        plt.savefig(picturename)
        plt.close()
'''
'''
count = 0
time_Wspeed = []  ###垂直速度，散度用
for i in wenjian_timename:
    if i == '2021071900' or count == 1:
        time_Wspeed.append(i)
        count = 1

hight_Wspeed = 500
###2021年7月19日00时-22日18时 500hPa 垂直速度
for time_i in time_Wspeed:
    ax, fig = createmap()
    colorbar = ax.contourf(lons, lats, W_speed[level_uv.index(hight_Wspeed), wenjian_timename.index(time_i), :, :],
                           cmap='Spectral',transform=ccrs.PlateCarree())
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    titlename = str(hight_Wspeed) + '_' + shijianchuli(wenjian_timename[wenjian_timename.index(time_i)]) + '时垂直速度'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\垂直速度'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()
###2021年7月19日00时-22日18时 500hPa 垂直速度修正
for time_i in time_Wspeed:
    ax, fig = createmap()
    colorbar = ax.contourf(lons, lats, W_speed_Xiu[level_uv.index(hight_Wspeed), wenjian_timename.index(time_i), :, :],
                           cmap='Spectral',transform=ccrs.PlateCarree())
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    titlename = str(hight_Wspeed) + '_' + shijianchuli(wenjian_timename[wenjian_timename.index(time_i)]) + '时垂直速度修正'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\垂直速度修正'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()

###2021年7月19日00时-22日18时 500hPa 散度 35N 垂直剖面
for time_i in time_Wspeed:
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1)
    colorbar = colorbar = ax.contourf(lons[40:51], levels, div_Xiu[:, wenjian_timename.index(time_i), 14, 40:51],
                                      cmap='Spectral')
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    #####横坐标显示经度
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    ax.xaxis.set_major_formatter(lon_formatter)
    ####纵坐标格式显示
    ax.invert_yaxis()
    ax.set_yscale('symlog')
    ##暴力显示
    plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100],
               ["1000", "900", "800", "700", "600", "500", "400", "300", "200", "100"])
    ax.set_ylabel('hPa')

    titlename = shijianchuli(wenjian_timename[wenjian_timename.index(time_i)]) + '时散度纬向剖面图'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\散度纬向剖面图'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()

###
'''
count = 0
time_5 = []  ###实习三（5）用
for i in wenjian_timename:
    if i == '2021072000' or count == 1:
        time_5.append(i)
        count = 1
hight_5 = 200
denghgtlines_Jiange = np.arange(-1000, 1500, 4)

###2021年7月20日00时-22日18时 200hPa 位势高度场，风场，高空急流（填色，>=30m/s)
for time_i in time_5:
    ax, fig = createmap()
    dengHGTlines = ax.contour(lons, lats, hgt[level_uv.index(hight_5), wenjian_timename.index(time_i), :, :],
                              colors='b',
                              linewidths=0.8, levels=denghgtlines_Jiange,
                              linestyles='-', extend='both',
                              transform=ccrs.PlateCarree())
    plt.clabel(dengHGTlines, inline=True, fontsize=8, fmt='%.0f')
    wind_slice = (slice(None, None, 2), slice(None, None, 2))  ####调风羽的密度
    uwind_huanliu = np.array(uwind[level_uv.index(hight_5), wenjian_timename.index(time_i), :, :])
    vwind_huanliu = np.array(vwind[level_uv.index(hight_5), wenjian_timename.index(time_i), :, :])
    plt.barbs(lon[wind_slice], lat[wind_slice], uwind_huanliu[wind_slice], vwind_huanliu[wind_slice],
              pivot='middle', length=4, barb_increments=dict(half=2, full=4, flag=20),
              color='black', transform=ccrs.PlateCarree())
    #########[x,y,u,v]  这四个都要 ndarray 形式
    hechengfeng = np.zeros((rh.shape[2], rh.shape[3]))
    for y in range(rh.shape[2]):
        for x in range(rh.shape[3]):
            hechengfeng[y, x] = sqrt(uwind_huanliu[y, x] ** 2 + vwind_huanliu[y, x] ** 2)
            if not hechengfeng[y, x] >= 30:
                hechengfeng[y, x] = np.NAN
    colorbar = ax.contourf(lons, lats, hechengfeng[:, :], colors='darkmagenta',
                           transform=ccrs.PlateCarree())
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    titlename = str(hight_5) + '_' + shijianchuli(wenjian_timename[wenjian_timename.index(time_i)]) + '时位势高度_风场_高空急流'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()  ###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\实习三5问'
    if not os.path.exists(picturepath):  ##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()
'''

shuiqitongliang_level = []
for i in rh_level.data:
    shuiqitongliang_level.append(str(i))

###水汽通量和水汽通量散度
for h_i in range(len(shuiqitongliang_level)):
    for time_i in range(len(time)):
        ax, fig = createmap()
        es[:, :] = 6.1078 * np.exp(a * (Temp[h_i, time_i, :, :]) / (Temp[h_i, time_i, :, :] + 273.16 - b))
        e[:, :] = Theta_rh[h_i, time_i, :, :] * es / 100
        q[:, :] = 0.622 * e[:, :] / (rh_P[h_i] - 0.378 * e[:, :])  # g/g
        uwind_shuiqi = np.array(uwind[h_i, time_i, :, :])*(units.m / units.s)
        vwind_shuiqi = np.array(vwind[h_i, time_i, :, :])*(units.m / units.s)
        u_shuiqi = np.array(uwind_shuiqi * q / constants.g)
        v_shuiqi = np.array(vwind_shuiqi * q / constants.g)
        div_shuiqi = mpcalc.divergence(u_shuiqi, v_shuiqi, dx=dx, dy=dy)
        colorbar = ax.contourf(lons, lats, div_shuiqi, cmap='nipy_spectral', transform=ccrs.PlateCarree())
        plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
        ##矢量
        wind_slice = (slice(None, None, 1), slice(None, None, 1))  ####调密度
        plt.quiver(lon[wind_slice], lat[wind_slice], u_shuiqi[wind_slice], v_shuiqi[wind_slice], transform=ccrs.PlateCarree())
        #########[x,y,u,v]  这四个都要 ndarray 形式
        titlename = shuiqitongliang_level[h_i] + '_' + shijianchuli(
            wenjian_timename[time_i]) + '时水汽通量和水汽通量散度'
        ax.set_title(titlename)
        ax.grid()
        plt.tight_layout()###让图填充整个画布
        picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\水汽通量和水汽通量散度\\' + shuiqitongliang_level[h_i]
        if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
            os.makedirs(picturepath)
        picturename = picturepath + '\\' + titlename + '.png'
        plt.savefig(picturename)
        plt.close()

zhengzhou_lat = 14
zhengzhou_lon = 45
q_chuizhi = np.zeros((len(shuiqitongliang_level), len(time), rh.shape[2], rh.shape[3]))
es_chuizhi = np.zeros((len(shuiqitongliang_level), len(time), rh.shape[2], rh.shape[3]))
e_chuizhi = np.zeros((len(shuiqitongliang_level), len(time), rh.shape[2], rh.shape[3]))
for h_i in shuiqitongliang_level:
    for time_i in range(len(time)):
        es_chuizhi[shuiqitongliang_level.index(h_i), time_i, :, :] = 6.1078 * np.exp(
            a * (Temp[shuiqitongliang_level.index(h_i), time_i, :, :]) / (
                    Temp[shuiqitongliang_level.index(h_i), time_i, :, :] + 273.16 - b))
        e_chuizhi[shuiqitongliang_level.index(h_i), time_i, :, :] = Theta_rh[shuiqitongliang_level.index(h_i), time_i,
                                                                    :, :] * es_chuizhi[shuiqitongliang_level.index(h_i),
                                                                            time_i, :, :] / 100
        q_chuizhi[shuiqitongliang_level.index(h_i), time_i, :, :] = 0.622 * e_chuizhi[shuiqitongliang_level.index(h_i),
                                                                            time_i, :, :] / (
                                                                            rh_P[shuiqitongliang_level.index(
                                                                                h_i)] - 0.378 * e_chuizhi[
                                                                                                shuiqitongliang_level.index(
                                                                                                    h_i),
                                                                                                time_i, :, :])  # g/g

###W-v流场，叠加水汽经向剖面图,112.5E
for time_i in range(len(time)):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1)
    colorbar = ax.contourf(lat_rh2, level_rh2, q_chuizhi[:, time_i, :, zhengzhou_lon], cmap='nipy_spectral')
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    plt.quiver(lat_rh2, level_rh2,
                  vwind[:len(shuiqitongliang_level), time_i, :, zhengzhou_lon],
                  W_speed_Xiu[:len(shuiqitongliang_level), time_i, :, zhengzhou_lon])
    #####横坐标显示维度
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lat_formatter)
    ####纵坐标格式显示
    ax.invert_yaxis()
    ax.set_yscale('symlog')
    ##暴力显示
    plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300], ["1000", "900", "800", "700", "600", "500", "400", "300"])
    ax.set_ylabel('hPa')
    titlename = shijianchuli(wenjian_timename[time_i]) + '时W-v流场，叠加水汽经向剖面图'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\W-v流场，叠加水汽经向剖面图\\'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()
###W-u流场，叠加水汽经向剖面图,35N
for time_i in range(len(time)):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.subplots(1, 1)
    colorbar = ax.contourf(lon_rh1, level_rh1, q_chuizhi[:, time_i, zhengzhou_lat, :], cmap='nipy_spectral')
    plt.colorbar(colorbar, extendrect='True', pad=0.03, fraction=0.04, shrink=1)
    plt.quiver(lon_rh1, level_rh1,
                  uwind[:len(shuiqitongliang_level), time_i, zhengzhou_lat, :],
                  W_speed_Xiu[:len(shuiqitongliang_level), time_i, zhengzhou_lat, :])
    #####横坐标显示经度
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    ax.xaxis.set_major_formatter(lon_formatter)
    ####纵坐标格式显示
    ax.invert_yaxis()
    ax.set_yscale('symlog')
    ##暴力显示
    plt.yticks([1000, 900, 800, 700, 600, 500, 400, 300], ["1000", "900", "800", "700", "600", "500", "400", "300"])
    ax.set_ylabel('hPa')
    titlename = shijianchuli(wenjian_timename[time_i]) + '时W-u流场，叠加水汽维向剖面图'
    ax.set_title(titlename)
    ax.grid()
    plt.tight_layout()###让图填充整个画布
    picturepath = 'D:\\python\\tianzhen\\shixi3_4\\picture\\W-u流场，叠加水汽维向剖面图\\'
    if not os.path.exists(picturepath):##判断文件夹是否存在，不存在就创建一个新的
        os.makedirs(picturepath)
    picturename = picturepath + '\\' + titlename + '.png'
    plt.savefig(picturename)
    plt.close()

'''
'''
分别绘制在32.5-35N内平均850hPa水汽通量，水汽通量的风场散度项和水汽通量的水汽平流项的经度-时间剖面图
（时间从2021年7月19日-22日18时，经度从100-125E）
'''
'''
ex45_level = 850
count = 0
ex45_time = []
for i in wenjian_timename:
    if i == '2021071900' or count == 1:
        ex45_time.append(i)
        count = 1

###850hPa水汽通量散度
fig = plt.figure(figsize=(9, 6))
ax = fig.subplots(1, 1)
div_shuiqi = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))
for h_i in range(len(shuiqitongliang_level)):
    for time_i in range(len(time)):
        es[:, :] = 6.1078 * np.exp(a * (Temp[h_i, time_i, :, :]) / (Temp[h_i, time_i, :, :] + 273.16 - b))
        e[:, :] = Theta_rh[h_i, time_i, :, :] * es / 100
        q[:, :] = 0.622 * e[:, :] / (rh_P[h_i] - 0.378 * e[:, :])  # g/g
        uwind_shuiqi = np.array(uwind[h_i, time_i, :, :]) * (units.m / units.s)
        vwind_shuiqi = np.array(vwind[h_i, time_i, :, :]) * (units.m / units.s)
        u_shuiqi = np.array(uwind_shuiqi * q / constants.g)
        v_shuiqi = np.array(vwind_shuiqi * q / constants.g)
        div_shuiqi[h_i, time_i, :, :] = mpcalc.divergence(u_shuiqi, v_shuiqi, dx=dx, dy=dy)
plt.contourf(lons[40:51], ex45_time,
             (div_shuiqi[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 14, 40:51] +
              div_shuiqi[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 13, 40:51]) / 2,
             cmap='Spectral')
plt.colorbar()
#####横坐标显示经度
lon_formatter = LongitudeFormatter(zero_direction_label=False)
ax.xaxis.set_major_formatter(lon_formatter)
ax.set_title('shixi45_850hPa水汽通量散度')
ax.grid()
plt.tight_layout()###让图填充整个画布
plt.savefig('D:\\python\\tianzhen\\shixi3_4\\picture\\shixi45_850hPa水汽通量散度.png')
plt.close()

###风的散度
fig = plt.figure(figsize=(9, 6))
ax = fig.subplots(1, 1)
plt.contourf(lons[40:51], ex45_time,
             (div_Xiu[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 14, 40:51] +
              div_Xiu[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 13, 40:51]) / 2,
             cmap='Spectral')
plt.colorbar()
#####横坐标显示经度
lon_formatter = LongitudeFormatter(zero_direction_label=False)
ax.xaxis.set_major_formatter(lon_formatter)
ax.set_title('shixi45_850hPa风散度')
ax.grid()
plt.tight_layout()###让图填充整个画布
plt.savefig('D:\\python\\tianzhen\\shixi3_4\\picture\\shixi45_850hPa风散度.png')
plt.close()

###水汽通量平流
fig = plt.figure(figsize=(9, 6))
ax = fig.subplots(1, 1)
adv_shuiqi = np.zeros((rh.shape[0], rh.shape[1], rh.shape[2], rh.shape[3]))
for h_i in range(len(shuiqitongliang_level)):
    for time_i in range(len(time)):
        es[:, :] = 6.1078 * np.exp(a * (Temp[h_i, time_i, :, :]) / (Temp[h_i, time_i, :, :] + 273.16 - b))
        e[:, :] = Theta_rh[h_i, time_i, :, :] * es / 100
        q[:, :] = 0.622 * e[:, :] / (rh_P[h_i] - 0.378 * e[:, :])  # g/g
        uwind_shuiqi = np.array(uwind[h_i, time_i, :, :]) * (units.m / units.s)
        vwind_shuiqi = np.array(vwind[h_i, time_i, :, :]) * (units.m / units.s)
        u_shuiqi = np.array(uwind_shuiqi * q / constants.g)
        v_shuiqi = np.array(vwind_shuiqi * q / constants.g)
        adv_shuiqi[h_i, time_i, :, :] = mpcalc.advection(u_shuiqi, v_shuiqi, dx=dx, dy=dy)
plt.contourf(lons[40:51], ex45_time,
             (adv_shuiqi[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 14, 40:51] +
              adv_shuiqi[level_uv.index(ex45_level), wenjian_timename.index(ex45_time[0]):, 13, 40:51]) / 2,
             cmap='Spectral')
plt.colorbar()
#####横坐标显示经度
lon_formatter = LongitudeFormatter(zero_direction_label=False)
ax.xaxis.set_major_formatter(lon_formatter)
ax.set_title('shixi45_850hPa水汽通量平流')
ax.grid()
plt.tight_layout()###让图填充整个画布
plt.savefig('D:\\python\\tianzhen\\shixi3_4\\picture\\shixi45_850hPa水汽通量平流.png')
plt.close()
'''
