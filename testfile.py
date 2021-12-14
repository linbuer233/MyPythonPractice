import xarray as xr
a=xr.open_mfdataset('D:\\python\\tianzhen\\1980-2010airsurface\\air.*.nc')
a.to_netcdf('D:\\python\\tianzhen\\1980-2010airsurface\\3.nc')