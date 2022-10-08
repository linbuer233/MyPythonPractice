import difflib
import filecmp
def compare_file():
    f = open('./cppy.py','r',encoding='utf-8')
    a = f.read()
    f.close()
    f = open('D:\\WORKcode\\pythoncode\\python_practice\\台风相关绘图\\cppy.py','r',encoding='utf-8')
    b = f.read()
    f.close()
    compare = difflib.HtmlDiff()
    c = compare.make_file(a,b)
    f = open('c.html','w')
    f.write(c)
    f.close()
# compare_file()
import os
print(filecmp.cmp('./cppy.py','D:\\WORKcode\\pythoncode\\python_practice\\台风相关绘图\\cppy.py'))