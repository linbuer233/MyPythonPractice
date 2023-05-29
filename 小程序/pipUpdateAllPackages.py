"""
实现用 pip 更新所有的包，类似于 conda 的 conda update --all
"""

import os

a = os.popen("pip list")
b = a.readlines()

for i in b[2:]:
    for j in i:
        if j == " ":
            end = i.index(j)
            break
    command = "pip install --upgrade" + i[0:end] + " -U"
    os.system(command)
