import numpy as np


def fei(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n >= 2:
        return fei(n - 1) + fei(n - 2)


a = []
for i in range(14):
    a.append(fei(i))
print(a)

b = np.array([[True, False],
              [True, True]])
c = np.arange(4).reshape(2, 2)
d = np.arange(2,6,1).reshape(2,2)
d[np.where(c > 1)]
print(d[c>1])
