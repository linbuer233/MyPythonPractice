# 下载leida
def downloadld(txtpath, picturepath):
    import pandas as pd
    import requests
    import os

    picture_url = pd.read_csv(txtpath, header=None)
    for i in range(len(picture_url)):
        img_url = str(picture_url.loc[i].values[0])
        name = img_url[96:121]
        year = name[13:17]
        month = name[17:19]
        day = name[19:21]
        # 通过url读取图片信息
        page = requests.get(img_url)
        # 转为二进制图片
        img = page.content
        '''
        存放图片
        '''
        img_path = picturepath + "\\" + year + "\\" + month + "\\" + day
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        with open(img_path + "\\" + name + ".png", mode='wb') as f:
            f.write(img)


print("输入的路径斜杠是\\", "\n")
txtpath = input()
picturepath = '/d/Project/DL_leida_rain/data'
downloadld(txtpath, picturepath)
