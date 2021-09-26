#!/home/scbmark/anaconda3/bin/python3.8
#爬取av01的封面圖
#作者：scbmark
#日期：2021/9/19
#版本：5.0(python)

from bs4 import BeautifulSoup
from requests import get,post
import sys
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog as fd
import shelve

defaultpath='/run/media/scbmark/Data/user/Downloads/006 AV_tem/'
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
    keywd=input("搜尋：")
    if keywd=="q":
        sys.exit("程式結束")
    else:
        data={"sn":f'{keywd}'}
        # 取得html檔
        root=post(url,headers=headers,data=data)

        # 解析html
        htmlfile=BeautifulSoup(root.text,"lxml")

        # 印出標題、片商、女優、發行日
        try:
            movinfo=htmlfile.find("h3")

            num=movinfo.small.string[0:movinfo.small.string.index(' ')].upper()
            address=movinfo.small.string[movinfo.small.string.index(' ')+1:]
            title=movinfo.getText().strip(movinfo.small.string)

            movfile=shelve.open(defaultpath+'movfile_tem')
            movfile[f'{num}']=[num,address,title]
            movfile.close()

            print('\n-----影片資訊-----')
            print('番號：'+num.upper())
            print('女優：'+address)
            print('標題：'+title)
            
            # 找出封面圖的標籤位置和網址
            print('\n圖片下載中...')
            img=htmlfile.find("div", class_="col-xs-12 col-md-12").find("img")
            imglink=img["src"]

            # 下載封面圖並存檔
            img=get(imglink,headers=headers)
            imgnam=dowwloadpath+num+".jpg"
            with open(imgnam,"wb") as file:
                file.write(img.content)
                print('-----下載完成-----\n')
            file.close()
        except:
            print('查無資料')
            continue
