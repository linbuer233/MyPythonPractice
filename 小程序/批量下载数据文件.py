import wget
import os 

PATH="{下载的文件存放的路径}"
if not os.path.exists(PATH):
        os.makedirs(PATH)
for i in range(1979,2023,1):
    url= " {你要下载的文件的地址 }"

    file_name = wget.filename_from_url(url)## 获取文件名 就是链接最后一串 
    
    if os.path.exists(os.path.join(PATH,file_name)):
        continue
    print("下载\t",file_name)
    
    wget.download(url,out = os.path.join(PATH,file_name))
    print("\n")