'''
2022/1/18
实现计算文件里（纯文本文件）的字母个数
'''
import numpy as np


def word_count(path):
    f = open(path, "r")
    a = f.read()
    word = list(np.arange(65, 91, 1))
    bigcount = np.zeros(26)
    smallcount = np.zeros(26)
    allcount = np.zeros(26)
    for i in a:
        for j in word:
            if ord(i) == j:
                bigcount[word.index(j)] = bigcount[word.index(j)] + 1

            if ord(i) == j + 32:
                smallcount[word.index(j)] = smallcount[word.index(j)] + 1
    allcount = bigcount + smallcount
    print("字母\t数量\t字母数量")
    print("---------------------------------------------")
    for i in word:
        print(chr(i), ":", "\t", str(bigcount[word.index(i)]), " | ", chr(i + 32), ":", "\t",
              str(smallcount[word.index(i)]),
              " | ", "总共:", allcount[word.index(i)])
        print("---------------------------------------------")


word_count("D:\\WORKcode\\1.txt")
