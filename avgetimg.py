#!/home/scbmark/anaconda3/bin/python3.8
#爬取av01的封面圖
#作者：scbmark
#日期：2021/9/15
#版本：3.0(python)

from bs4 import BeautifulSoup
from requests import get,post
import sys
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog as fd

defaultpath='/run/media/scbmark/Data/user/Downloads/'
print(f"程式啟動\n預設下載位置：\n{defaultpath}\n")

t=0
while t==0:
    chgdir=input('是否更改下載位置(y=1,n=2)')
    if int(chgdir)==1:
        root = Tk()
        root.withdraw()
        root.directory = fd.askdirectory(initialdir = Path.home())
        dowwloadpath=root.directory+'/'
        print ('新的下載位置：'+dowwloadpath)
        t=1
    elif int(chgdir)==2:
        dowwloadpath=defaultpath
        t=1
    else:
        print('輸入錯誤')

#av01的搜尋主機名
url="https://www.jav321.com/search"
headers={
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

t=0
while t==0:
    # 輸入番號
    print("\n請輸入番號 例如:mide-365 ,mide365 或輸入'q'結束程式")
    num=input("番號：")
    if num=="q":
        sys.exit("程式結束")
    else:
            data={"sn":f'{num}'}
            # 取得html檔
            root=post(url,headers=headers,data=data)

            # 解析html
            htmlfile=BeautifulSoup(root.text,"lxml")

            # 印出標題、片商、女優、發行日
            title=htmlfile.find("h3")
            print('標題：'+title.getText().strip(title.small.string))
            movinfo=htmlfile.find("div",class_="col-md-9")
            pro_actress=movinfo.find_all("a",limit=2)
            print('片商：'+pro_actress[1].string)
            print('女優：'+pro_actress[0].string)

            # 找出封面圖的標籤位置和網址
            print('\n圖片下載中...')
            img=htmlfile.find("div", class_="col-xs-12 col-md-12").find("img")
            imglink=img["src"]
            
            # 下載封面圖並存檔
            img=get(imglink,headers=headers)
            filename=title.small.string[0:title.small.string.index(' ')]
            imgnam=dowwloadpath+filename.upper()+".jpg"
            with open(imgnam,"wb") as file:
                file.write(img.content)
                print('-----下載完成-----\n')
            file.close()
