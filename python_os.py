import os

# 遍历文件 利用os的walk函数实现

import numpy as np

level=[]
def walkFile(file):
    for root, dirs, files in os.walk(file):
        # root 表示正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # print(os.walk(file))
        # print(root)
        # print(files)

        #####按数字大小排列，而不是字符串大小
        a = np.zeros(len(dirs))
        for i in dirs:
            a[dirs.index(i)] = float(i)
        ##### 冒泡排序
        # for i in range(len(dirs)):
        #     for j in range(len(dirs) - i - 1):
        #         if a[j] > a[j + 1]:
        #             temp = a[j]
        #             a[j] = a[j + 1]
        #             a[j + 1] = temp
        b = list(np.sort(a))
        for i in b:
            dirs[b.index(i)] = str(int(i))
        ###########################
        ###遍历文件  os.path.join(a,b)是把a和b 合为一个路径
        # for f in files:
        #     print(os.path.join(root, f))
        ###遍历所有文件夹
        level.append(dirs)
        print(len(dirs),level)
        for d in dirs:
            # print(os.path.join(root, d))
            a=os.listdir(os.path.join(root,d))
            for i in a:
                a[a.index(i)] = i[:-4]


def main():
    walkFile('d:\\python\\tianzhen\\shixi2\\air')


if __name__ == '__main__':
    main()
level_a=np.array(level)
print(len(level))
print(level[0])