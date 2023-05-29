import random as rd

import numpy as np
import pandas as pd


def readnum():
    fd = pd.read_excel('体彩大乐透 - 问卷统计详情.xlsx')
    name = fd.iloc[5:, 0].values
    f5 = fd.iloc[5:, 8].values
    b2 = fd.iloc[5:, 9].values
    return name, f5, b2


# 返回 bool 列表，方便后续去除数字不够，网址的同学
def TFfun(df, string, num):
    alist = []
    for i in df[string]:
        if len(i) > 40:
            alist.append(False)
            continue
        count = 0
        for j in i:
            try:
                j = int(j)
            except:
                j = str(j)
                if j == ',' or j == '，':
                    count += 1
        alist.append(count == num)
    return alist


# 提取抽奖的号码
"""
每人的抽奖号码中前面的数字通过后面的逗号或空格区别，因为他们没法变成整型，最坏一数字通过循环结束区别
"""


def coulist1(newdf, string):
    list5 = []
    for i in newdf[string]:
        temp = []
        temp1 = []
        for j in i:
            try:
                j = int(j)
                temp.append(j)
            except:
                if temp == []:
                    continue
                a = ''
                for i in temp:
                    a = a + str(i)
                temp1.append(a)
                temp = []
        a = ''
        for i in temp:
            a = a + str(i)
        temp1.append(a)
        list5.append(temp1)
    return list5


# 随机生成一个抽奖列表
"""
随机生成，如果已经存在，再重新生成一个，直到没有或满
"""


def coulist(num, st, end):
    coulist = []
    count = 0
    while True:
        temp = rd.randint(st, end)
        if temp in coulist:
            continue
        coulist.append(temp)
        count += 1
        if count == num:
            break
    return coulist


def jiangxiang(f5num, b2num):
    if f5num == 5 and b2num == 2:
        return '一等奖'
    if f5num == 5 and b2num == 1:
        return '二等奖'
    if f5num == 5 and b2num == 0:
        return '三等奖'
    if f5num == 4 and b2num == 2:
        return '四等奖'
    if f5num == 4 and b2num == 1:
        return '五等奖'
    if f5num == 3 and b2num == 2:
        return '六等奖'
    if f5num == 4 and b2num == 0:
        return '七等奖'
    if f5num == 3 and b2num == 1:
        return '八等奖'
    if f5num == 2 and b2num == 2:
        return '八等奖'
    if f5num == 3 and b2num == 0:
        return '九等奖'
    if f5num == 2 and b2num == 1:
        return '九等奖'
    if f5num == 1 and b2num == 2:
        return '九等奖'
    if f5num == 0 and b2num == 2:
        return '九等奖'
    else:
        return 0


# 查看是否中奖，中啥奖
"""
通过计算号码相同的个数实现
"""


def cou(f2l, b2l):
    f5num = 0
    b2num = 0
    for i in f2l:
        if i in f5coulist:
            f5num += 1
    for i in b2l:
        if i in b2coulist:
            b2num += 1
    return jiangxiang(f5num, b2num)


# 创建一个字典计数器，再把它添加到一个列表中，再拿另外一个列表放名字，通过元素的位置来区分，每人的中奖情况
def zhongjiangmingdan(ZJname, ZJlist, f2l, b2l, i):
    if i not in ZJname:
        ZJname.append(i)
        ZJdict = {}
        ZJdict[cou(f2l, b2l)] = 1
        ZJlist.append(ZJdict)
    else:
        inDEX = ZJname.index(i)
        if cou(f2l, b2l) not in ZJlist[inDEX]:
            ZJlist[inDEX][cou(f2l, b2l)] = 1
        else:
            ZJlist[inDEX][cou(f2l, b2l)] += 1


if __name__ == '__main__':
    name, f5, b2 = readnum()

    df = pd.DataFrame({'姓名': name, '前五个数字': f5, '后两个数字': b2})
    df = df.dropna()  # 去除 Nan 值
    ## 去除 nan 值之后，重置顺序
    df = pd.DataFrame(
        {'姓名': list(df['姓名']), '前五个数字': list(df['前五个数字']), '后两个数字': list(df['后两个数字'])})

    # 去除那些数字的不够的同学
    droplist5 = TFfun(df, '前五个数字', 4)
    droplist2 = TFfun(df, '后两个数字', 1)

    # 手动实现交集
    TFlist = []
    for i in range(len(droplist2)):
        if droplist2[i] == droplist5[i] and droplist2[i] == True:
            TFlist.append(True)
        else:
            TFlist.append(False)

    # 筛选出合格的抽奖同学
    newdf = df.iloc[TFlist]

    # 提取抽奖号码
    list5 = coulist1(newdf, '前五个数字')
    list2 = coulist1(newdf, '后两个数字')

    # 把 list5 的元素转成整型
    for i in range(len(list5[0][:])):
        for j in range(len(list5)):
            list5[j][i] = int(list5[j][i])
    # 把 list2 的元素转成整型
    for i in range(len(list2[0][:])):
        for j in range(len(list2)):
            list2[j][i] = int(list2[j][i])

    # 重新生成一个 DataFrame
    coujiang = pd.DataFrame({'name': list(newdf['姓名']), 'f5': list5, 'b2': list2})

    # 创建一个计数器，再把它添加到一个列表中，再拿另外一个列表放名字，通过元素的位置来区分，每人的中奖情况
    ZJlist = []
    ZJname = []

    # 抽一千次
    for _ in range(1000):
        f5coulist = coulist(5, 1, 35)
        b2coulist = coulist(2, 1, 12)
        for i in range(len(coujiang)):
            if cou(coujiang.loc[i]['f5'], coujiang.loc[i]['b2']) != 0:
                zhongjiangmingdan(ZJname, ZJlist, coujiang.loc[i]['f5'], coujiang.loc[i]['b2'],
                                  coujiang.loc[i]['name'])

    # 把中奖结果放到 dataframe
    ds1 = pd.DataFrame.from_dict(ZJlist[:])
    namedf = pd.DataFrame({'姓名': ZJname})
    ds2 = ds1.join(namedf)
    # 重新排列列的顺序
    ds2 = ds2[['姓名', '九等奖', '八等奖', '七等奖', '六等奖', '五等奖']].replace(np.nan, 0)
    print(ds2)
