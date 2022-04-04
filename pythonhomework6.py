import pandas as pd

df = pd.read_csv('rmm.74toRealtime.txt', header=None, skiprows=2, sep='\s+')
varname = {'0': 'year', '1': 'month', '2': 'day', '3': 'RMM1', '4': 'RMM2', '5': 'phase', '6': 'amplitude',
           '7': 'final_values'}
df.rename(columns=varname)
df.to_csv('pythonhomework6csv.csv')
df.to_excel('pythonhomework6excel.xlsx')
