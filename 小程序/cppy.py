import os
import glob
import filecmp  # 判断文件是否相同

benpath = os.getcwd()
benfile = glob.glob(benpath + '\\*\\*') + os.listdir()
aimfile = os.listdir("D:\\WORKcode\\pythoncode\\python_practice\\台风相关绘图")
benfile1 = []
# print(c)
# 首先把本文件夹下的目标文件夹不存在的 文件 复制过去
for i in benfile:
    if (".py" in i) or (".ipynb" in i):
        benfile1.append(i.split('\\')[-1])
        if (not os.path.exists('D:\WORKcode\pythoncode\python_practice\台风相关绘图\\' + i.split('\\')[-1])) or (
                not filecmp.cmp(i, 'D:\WORKcode\pythoncode\python_practice\台风相关绘图\\' + i.split('\\')[-1])):
            print('add', i)
            os.system("cp " + i + " D:\\WORKcode\\pythoncode\\python_practice\\台风相关绘图")
# 然后把目标文件夹存在，但本文件夹不存在的文件 删除
for j in aimfile:
    # print(j)
    if j not in benfile1:
        print('del:', j)
        os.system('del ' + 'D:\WORKcode\pythoncode\python_practice\台风相关绘图\\' + j)
