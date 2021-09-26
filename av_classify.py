#!/home/scbmark/anaconda3/bin/python3.8
# 分類資料夾中的AV檔案
# 作者：蕭丞伯
# 日期：2021/9/18
# 版本：1.0(python)

import os
import glob
from shutil import move
from pathlib import Path
from bs4 import BeautifulSoup
from requests import get, post
import shelve

root_path=Path.cwd()
totle_lists=glob.glob('*.jpg')
print(totle_lists)

movfile=shelve.open('movfile_tem')

for list in totle_lists:
    num=list[0:-4]
    oldName = Path(list).name
    newName = Path(list).stem.upper() + Path(list).suffix
    os.rename(oldName,newName)

    if num in movfile:
        address_name=movfile[f'{num}'][1]
        if address_name!='':
            if os.path.exists(address_name)==False:
                os.makedirs(address_name)
                move(fr'{list}', fr'{address_name}')
            else:
                move(fr'{list}', fr'{address_name}')
        else:
            if os.path.exists('undefine')==False:
                os.makedirs('undefine')
                move(fr'{list}', 'undefine')
            else:
                move(fr'{list}', 'undefine')
    else:
        print('查無本地資料')
        continue

totle_lists=glob.glob('*.mp4')
print(totle_lists)
for list in totle_lists:
    num=list[0:-4]
    oldName = Path(list).name
    newName = Path(list).stem.upper() + Path(list).suffix
    os.rename(oldName,newName)
    print(num)
    if num in movfile:
        address_name=movfile[f'{num}'][1]
        if address_name!='':
            if os.path.exists(address_name)==False:
                os.makedirs(address_name)
                move(fr'{list}', fr'{address_name}')
            else:
                move(fr'{list}', fr'{address_name}')
        else:
            if os.path.exists('undefine')==False:
                os.makedirs('undefine')
                move(fr'{list}', 'undefine')
            else:
                move(fr'{list}', 'undefine')
    else:
        print('查無本地資料')
        continue

movfile.close()