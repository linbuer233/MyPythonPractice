# import pandas as pd
#
# df = pd.read_csv('rmm.74toRealtime.txt', header=None, skiprows=2, sep='\s+')
# varname = {0: 'year', 1: 'month', 2: 'day', 3: 'RMM1', 4: 'RMM2', 5: 'phase', 6: 'amplitude', 7: 'final_values'}
# df = df.rename(columns=varname)
# df.to_csv('pythonhomework6csv.csv')
# df.to_excel('pythonhomework6excel.xlsx')


# 早些版本

import pandas as pd

with open("../../data/rmm.74toRealtime.txt", 'r') as f:
    f.readline()
    f.readline()
    rmm = f.readlines()
rmmall = []
varname = ['year', 'month', 'day', 'RMM1', 'RMM2', 'phase', 'amplitude', 'final_values']
for i in rmm:
    p = 0
    var_i = 0
    dict = {}
    count = 0
    for j in i:
        if j != ' ' and p == 0:
            st = count
            p = 1
            count += 1
            continue
        if j == ' ' and p == 1:
            end = count
            dict[varname[var_i]] = i[st:end]
            var_i += 1
            count += 1
            p = 0
            continue
        if j == '\n':
            dict[varname[var_i]] = i[st:count]
        count += 1
    rmmall.append(dict)

df = pd.DataFrame.from_dict(rmmall[:])
df.to_csv('../../data/pythonhomework6csv.csv')
df.to_excel('../../data/pythonhomework6excel.xlsx')
