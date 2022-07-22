# py-md5--爆破
基于py脚本的MD5爆破脚本
本脚本用于按照字典依次计算MD5值，然后以目录树的结构存储


存储结构(例如123)

md5
-2
--0
---2
----c
.........---202cb962ac59075b964b07152d234b70.txt



需要用到的库
import sys
import os
import hashlib
import atexit
import datetime
import json

运行  
python ./main.py

运行后会在当前运行路径生成一个md5的文件夹，即存储爆破结果的目录树


查询md5值参考示例
import os
import sys

path=__file__
path=path[0:(path.rfind('/'))-len(path)+1]

md5="54074e3bcfb67839e6eeddb2105c09ff"

path_md5 = "md5/" + "/".join(list(md5))  # md5/7/2/4/b/8/2/5/3/8/f/8/e/9/1/7/d/8/a/7/2/2/1/0/8/1/f/b/7/f/9/0/4

path2=path+path_md5+"/"+md5+".txt"
print(path2)

f= open(path2,"r",encoding="utf-8")
a=f.readline()
while a:
    print(a)
    a=f.readline()
f.close()





