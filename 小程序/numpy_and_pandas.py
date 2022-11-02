from math import *

import numpy as np

a = np.array([[1, 2, 3],
              [2, 3, 4]])
b = np.array([[1, 2, 3],
              [2, 3, 4]])

print(a + b)
#################################
print(a.ndim)  # 几维
# or
print(np.ndim(a))
#################################
print(a.shape)
# or
print(np.shape(a))
#################################
print(a.size)
# or
print(np.size(a))
# 生成0矩阵
c = np.zeros((3, 4), dtype=int)
print(c)
print('\n')
# 生成单位矩阵
c = np.eye(3, dtype=int)
print(c)
# 设置数组的格式
b = np.array([[1.111, 2, 3],
              [2, 3, 4]], dtype=float)
print(b)
print(b.dtype)

# 生成特殊数组
c = np.arange(12).reshape((3, 4))
print(c)

d = np.linspace(0, 2 * np.pi, 5)
print(d)

c = d * 10 ** 5
print(c)
print(sin(90 * pi / 180))
for i in range(4):
    titlename = '2' + str(i) + '-' + '2' + str(i + 1) + '日24小时变温'
    print(titlename)

# for i in datetime:
#     print(datetime.index(i))
