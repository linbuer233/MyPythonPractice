import os 
import glob 

a=os.getcwd()
b=glob.glob(a+'\\*\\*')+os.listdir()
# print(b)
for i in b:
    if (".py" in i) or (".ipynb" in i):
        print(i)
        os.system("cp "+i+" D:\\WORKcode\\pythoncode\\python_practice\\台风相关绘图")