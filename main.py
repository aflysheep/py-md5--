#redis本地爆破
#使用py逐一生城md5值
#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import hashlib
import atexit
import datetime
import json

# a=hashlib.md5("dd".encode())
# print(a.hexdigest())

####################
#exit_save.log   程序退出时的进度记录
#xiangtong.log     如果遇到2个md5相同的记录
#error.log      异常错误日志
#
#
#
#
#
#
#
#
#
#11111111111111111111111111111111
# 目录树结构
#最外36 最深36层次
#
#
#
#
#
# 1.py字典的生成
# 2.key-value的组成

dict='abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.*/-+ <>?:"{}_)(&^%$#@!`=[];\'\\,，。、|》《？：“~·'

#109字符

def str_ping(dict,num,len,str):
    str_len=len(str)
    if(str_len<len):
        str=str+dict[num]


#获取当前路径并锁定主目录，后续可自行更改  默认为./md5/
path=__file__
path=path[0:(path.rfind('/'))-len(path)+1]
path_xiangtong_log=path+"xiangtong.log"
path_exit_save_log=path+'exit_save.log'
path_try_error_log="error.log"

print(path)

print()






#获取当前日期时间 yyddmm hhssmm
def get_time():
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    return  time



# 错误日志记录
def error_save(path_err_log, value):
    f = open(path_err_log, 'a',encoding='utf-8')
    f.writelines(get_time()+"------"+value+"\n")
    f.close()


#相同md5值记录  #path 为程序根目录
#返回值1 写入成功  2 写入失败
def wirte_xiangtong_login(path_xiangtong_log,file_value):
    try:

        path_md5=hashlib.md5(file_value.encode()).hexdigest()

        f = open(path_xiangtong_log, "a",encoding="utf-8")
        f.writelines(get_time()+"------"+path_md5 + "------" + file_value + "\n")
        f.close()
        return 1
    except Exception:
        return -1




#读取文件计算MD5
def file_value_to_md5(path):
    try:
        f=open(path,'r',encoding="utf-8")
        file_value_md5=f.readline().rstrip("\n")
        f.close()
        file_value_md5=file_value_md5.encode()
        a=hashlib.md5(file_value_md5)
        return a.hexdigest()
    except Exception as e:

        return -1

# 判断路径md5值  文件MD5值   文件内容md5值 是否一致
#返回结果  1 全相同.-1路径名字md5和文件名md5不相同（一般不肯出现），2路径md5和内容MD5不相同，返回路径md5,文件名md5,和结果md5
def tf_path_md5_and_file_name_md5_and_file_name_md5(path,value_zhi):
    path_md5=path[path.rfind('md5')+4:path.rfind("/")].replace("/","")
    file_name_md5=path[path.rfind('/')+1:path.rfind('.')]
    file_value_md5=file_value_to_md5(path)
    f=open(path,"r",encoding="utf-8")
    a=f.readline().rstrip("\n")
    if(a==value_zhi):
        return 0,"success"
    elif(path_md5==file_name_md5==file_value_md5):
        return 1,"success"
    elif(path_md5!=file_name_md5):
        return -1,path_md5
    elif(path_md5!=file_value_md5):
        return 2,path_md5,file_name_md5,file_value_md5




#创建目录  如果目录1：创建成功 。0：目录已存在。-1：创建失败
def mkdir(path):
    try:
        path = path.strip()
        tf_mkdir = os.path.exists(path)
        if (tf_mkdir):
            return 0
        else:
            os.makedirs(path)
            return 1

    except Exception as e:
        return -1,e


#写入txt 将md5  本方法提供给touch调用的
def touch_white(path,value):
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    f = open(path, 'a',encoding="utf-8")
    f.writelines(value + "\n")
    f.close()

#创建文件   path 为绝对路径  value_zhi 为txt值
def touch(path,value_zhi):
    global path_xiangtong_log,path_try_error_log
    path =path.strip()

    #判断该文件是否存在
    tf_touch=os.path.exists(path)

    if(tf_touch):#存在
        file_size = os.path.getsize(path)
        if(file_size==0):
            touch_white(path,value_zhi)
            return
        elif(file_size>0):
            value = tf_path_md5_and_file_name_md5_and_file_name_md5(path,value_zhi)
            if(value[0]==0):
                error_save(path_try_error_log,"重连出现与上一个值相同，已跳过，跳过值为：{0}".format(value_zhi))
            elif (value[0] == 1):
                wirte_xiangtong_login(path_xiangtong_log,value_zhi)
                touch_white(path,value_zhi)
            elif(value[0]==2):
                error_save(path_try_error_log,"前一个的md5值错误,当前值：{0}，当前md5：{1}，旧md5：{2}".format(value_zhi,value[1],value[3]))
                touch_white(path, value_zhi)


    else:#不存在
        touch_white(path, value_zhi)





#初始化创建MD5目录
if mkdir(path+"md5")!=-1:
    print("mkdir md5 success")


# a=mkdir(path+"md5/e/1/0/a/d/c/3/9/4/9/b/a/5/9/a/b/b/e/5/6/e/0/5/7/f/2/0/f/8/8/3/e/")
# touch(path+"md5/e/1/0/a/d/c/3/9/4/9/b/a/5/9/a/b/b/e/5/6/e/0/5/7/f/2/0/f/8/8/3/e/"+"e10adc3949ba59abbe56e057f20f883e.txt","123456")



######以上是md5保存内容##########以下是字典生产内容##########################################################

#当前字典长度
dict_len=1    #当前的字典长度
dict_str=''   #当前的字典内容
dict_unm=[]  #存放的每一位数值从dict中查询到了第几个
dict_str_zhi=0




#字典初始化 //////////////////////////////////////////
# 推出处理器  如果程序意外退出停止，会记录下最后运行到了哪里
def exit_save(path_exit_save_log):
    global dict_len,dict_str,dict_unm,dict_str_zhi

    f = open(path_exit_save_log, 'w',encoding="utf-8")
    f.writelines("time:"+get_time()+"\n")
    f.writelines("dict_len:{0}".format(dict_len)+"\n")
    f.writelines("dict_str:{0}".format(dict_str)+"\n")
    f.writelines("dict_unm:{0}".format(json.dumps(dict_unm))+"\n")
    f.writelines("dict_str_zhi:{0}".format(dict_str_zhi)+"\n")
    f.close()


atexit.register(exit_save,path_exit_save_log)
def dict_init():
    global path_exit_save_log
    if(os.path.exists(path_exit_save_log)):
        dict_init=[]
        f=open(path_exit_save_log,'r',encoding="utf-8")
        a=f.readline()
        while a:
            a=f.readline()
            dict_len=a.split(':')[1].strip()
            a = f.readline()
            dict_str=a.split(':')[1].rstrip("\n")
            a = f.readline()
            dict_unm=json.loads(a.split(':')[1].strip())
            a=f.readline()

            dict_str_zhi=a.split(':')[1].strip()
            return dict_len,dict_str,dict_unm,dict_str_zhi
#字典写入测试方法
def cesi(value):
    f=open("./cs.txt",'a',encoding="utf-8")
    f.writelines(value+'\n')
    f.close()

def dict_ping():
    global dict_len,dict_str,dict_unm,dict,dict_str_zhi,path
    dict_str=""

#该while 为初始化dict_str  使得dict_str能补全正确的位数
    while len(dict_str)<dict_len:
        dict_str=dict_str+dict[0]
    while len(dict_unm)<dict_len:
        dict_unm.append(0)



    while 1:
        for i in range(dict_len):
            dict_str=list(dict_str)
            dict_str[i]=dict[dict_unm[i]]
            dict_str="".join(dict_str)
        print(dict_str)
        cesi(dict_str)

        md5=hashlib.md5(dict_str.encode()).hexdigest()  #9131a82712b7f86b33630420cbb4807c
        path_md5="md5/"+"/".join(list(md5))    #md5/7/2/4/b/8/2/5/3/8/f/8/e/9/1/7/d/8/a/7/2/2/1/0/8/1/f/b/7/f/9/0/4
        a=mkdir(path+path_md5)
        touch(path+path_md5+"/"+md5+".txt",dict_str)

        # if(dict_str=='·a'):
        #     print("aaa")

        dict_str_zhi=dict_str_zhi+1
        dict_unm[0]=dict_str_zhi
#dict_str_wei=109  第一遍结束
        if (dict_str_zhi == len(dict)):    #第第0值计满
            dict_str_zhi=0                 #第0位下表清0
            for i in range(len(dict_unm)):
                if(dict_unm[i]==len(dict)):   #判断是否达到进位条件
                    if(i==len(dict_str)-1):   #判断是否全部计数计满   计满需要dict_str 长度+1 即 dict_len+dict_len+1
                        dict_unm=[]
                        dict_str = dict_str + (dict[0])
                        dict_len=dict_len+1
                        while len(dict_unm)<dict_len:
                            dict_unm.append(0)

                        break
                    elif(i<len(dict_str)-1):
                        dict_unm[i]=0
                        dict_unm[i+1]=dict_unm[i+1]+1

if(os.path.exists(path_exit_save_log)):
    a=dict_init()
    dict_len =int( a[0])  # 当前的字典长度
    dict_str = a[1]  # 当前的字典内容
    dict_unm = a[2]  # 存放的每一位数值从dict中查询到了第几个
    dict_str_zhi =int( a[3])


dict_ping()


