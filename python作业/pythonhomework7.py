import struct

import pandas as pd
import xarray as xr

df = pd.read_csv('pythonhomework6csv.csv')
var = ['RMM1', 'RMM2']
with open('pythonhomework7bin.dat', 'wb') as f:
    for i in var:
        for j in df[i].values:
            temp = struct.pack('f', j)
            f.write(temp)

time = pd.date_range('1974-06-01', '2022-03-25', freq='1d')
ds = xr.Dataset({'RMM1': (['time'], df['RMM1']),
                 'RMM2': (['time'], df['RMM2']), },
                coords={'time': (['time'], time)})
ds.to_netcdf('pythonhomework7nc.nc')
