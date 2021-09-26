#!/home/scbmark/anaconda3/bin/python3.8
#爬取av的資訊/下載封面/分類資料夾中的AV檔案
#作者：scbmark
#日期：2021/9/26
#版本：1.0(python)

import sys
import os
import glob
import shelve
from pathlib import Path
from bs4 import BeautifulSoup
from requests import get,post
from shutil import move

def set_path():
    defaultpath='/run/media/scbmark/Data/user/Downloads/006 AV_tem/'
    print(f"預設路徑：\n{defaultpath}")
    t=0
    while t==0:
        chgdir=input('是否更改路徑：\n(y=1,n=2)')
        if int(chgdir)==1:
            from tkinter import Tk
            from tkinter import filedialog as fd
            root = Tk()
            root.withdraw()
            root.directory = fd.askdirectory(initialdir = Path.home())
            dowwloadpath=root.directory+'/'
            os.chdir(dowwloadpath)
            print ('新的路徑：\n'+dowwloadpath)
            t=1
        elif int(chgdir)==2:
            dowwloadpath=defaultpath
            os.chdir(dowwloadpath)
            t=1
        else:
            print('輸入錯誤')
    return dowwloadpath

def get_keywd():
    # 輸入番號
    print("\n請輸入番號 例如:mide-365 ,mide365 或輸入'q'結束程式")
    keywd=input("搜尋：")
    if keywd=="q":
        print('回主選單')
        print('--------------------')
        data=1
        # sys.exit("程式結束")
    else:
        data={"sn":f'{keywd}'}
    return data

def get_htmlfile(data):
    url="https://www.jav321.com/search"
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    # 取得html檔
    root=post(url,headers=headers,data=data)
    htmlfile=BeautifulSoup(root.text,"lxml")
    return htmlfile

def analyze_htmlfile(htmlfile, defaultpath):
    try:
        movinfo=htmlfile.find("h3")
        img=htmlfile.find("div", class_="col-xs-12 col-md-12").find("img")
        imglink=img["src"]

        num=movinfo.small.string[0:movinfo.small.string.index(' ')].upper()
        address=movinfo.small.string[movinfo.small.string.index(' ')+1:]
        title=movinfo.getText().strip(movinfo.small.string)
        avinfo=[num, address, title, imglink]
    except:
        print('無此番號資料')
        avinfo=[]
    return avinfo

def save_info(avinfo, dowwloadpath):
    movfile=shelve.open(dowwloadpath+'movfile_tem')
    movfile[f'{avinfo[0]}']=avinfo
    movfile.close()

def print_info(avinfo):
    print('\n-----影片資訊-----')
    print('番號：'+avinfo[0])
    print('女優：'+avinfo[1])
    print('標題：'+avinfo[2])
    print('--------------------')

def save_img(avinfo, dowwloadpath):
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    print('\n圖片下載中...')
    img=get(avinfo[3],headers=headers)
    imgnam=dowwloadpath+avinfo[0]+".jpg"
    with open(imgnam,"wb") as file:
        file.write(img.content)
        print('-----下載完成-----\n')
    file.close()

def file_catgory(dowwloadpath):
    movfile=shelve.open(dowwloadpath+'movfile_tem')
    filetype=('*.jpg', '*.mp4')
    totle_lists=[]
    unknown=[]
    for type in filetype:
        totle_lists.extend(glob.glob(type))
    print(totle_lists)
    print('-'*20)
    
    for list in totle_lists:
        oldName = Path(list).name
        newName = Path(list).stem.upper() + Path(list).suffix
        os.rename(oldName,newName)
        list=newName
        num=list[0:-4]
        
        if num in movfile:
            address_name=movfile[f'{num}'][1]
            if address_name!='':
                if os.path.exists(address_name)==False:
                    os.makedirs(address_name)
                    move(fr'{list}', fr'{address_name}')
                    print(f'{list}--移動完成')
                else:
                    move(fr'{list}', fr'{address_name}')
                    print(f'{list}--移動完成')
            else:
                if os.path.exists('002 undefine')==False:
                    os.makedirs('002 undefine')
                    move(fr'{list}', '002 undefine')
                    print(f'{list}--移動完成')
                else:
                    move(fr'{list}', '002 undefine')
                    print(f'{list}--移動完成')
        else:
            if num[0:3]=='FC2':
                if os.path.exists('001 FC2')==False:
                    os.makedirs('001 FC2')
                    move(fr'{list}', '001 FC2')
                    print(f'{list}--移動完成')
                else:
                    move(fr'{list}', '001 FC2')
                    print(f'{list}--移動完成')
            elif num[-2]=='-':
                num=num[0:-2]
                if num in movfile:
                    address_name=movfile[f'{num}'][1]
                    if address_name!='':
                        if os.path.exists(address_name)==False:
                            os.makedirs(address_name)
                            move(fr'{list}', fr'{address_name}')
                            print(f'{list}--移動完成')
                        else:
                            move(fr'{list}', fr'{address_name}')
                            print(f'{list}--移動完成')
                    else:
                        if os.path.exists('002 undefine')==False:
                            os.makedirs('002 undefine')
                            move(fr'{list}', '002 undefine')
                            print(f'{list}--移動完成')
                        else:
                            move(fr'{list}', '002 undefine')
                            print(f'{list}--移動完成')
                else:
                    print(f'{list}--查無本地資料')
                    unknown.extend(list)

            else:
                print(f'{list}--查無本地資料')
                unknown.append(list)
    print('--------------------')
    print('分類完成\n')
    if unknown!=[]:
        print('尚有以下未分類', unknown)
    movfile.close()
    return unknown


k=0
while k==0:
    mode=input('輸入模式：\n(1.下載資料和封面 2.檔案分類 3.離開)')
    if mode=='1':
        dowwloadpath=set_path()
        t=0
        while t==0:
            data=get_keywd()
            if data!=1:
                htmlfile=get_htmlfile(data)
                avinfo=analyze_htmlfile(htmlfile, dowwloadpath)
                if avinfo!=[]:
                    save_info(avinfo, dowwloadpath)
                    print_info(avinfo)
                    imglink=avinfo[3]
                    save_img(avinfo, dowwloadpath)
            else:
                break

    elif mode=='2':
        dowwloadpath=set_path()
        unknown=file_catgory(dowwloadpath)        
        if unknown!=[]:            
            for unknow in unknown:
                print(f'嘗試下載{unknow[0:-4]}的資料中...')
                data={"sn":f'{unknow[0:-4]}'}
                htmlfile=get_htmlfile(data)
                avinfo=analyze_htmlfile(htmlfile, dowwloadpath)
                save_info(avinfo, dowwloadpath)
                print_info(avinfo)
            file_catgory(dowwloadpath)
    elif mode=='3':
        sys.exit("程式結束")
    else:
        print('輸入錯誤')