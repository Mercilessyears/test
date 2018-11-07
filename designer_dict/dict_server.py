'''
name:Tedu
mondules:pymysql
This is a dict project for study
'''

import os,sys
from socket import *
import time
import pymysql
from threading import Thread
import time


# 1设计全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)
DICT_TEXT = "./dict.txt"

# 创建一个线程来处理僵尸进程
def zombie():
    os.wait()



# 2创建网络连接
def main():
    # 3创建数据库连接
    db = pymysql.connect("localhost","root","123456","dict")
    # 4创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(9)
    print("Listen the port 8080...")

    while True:
        try:
            c,addr = s.accept()
            print("连接用户端:",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("退出服务器")
        except Exception as e:
            print("服务器异常",e)
            continue
        
        # 5创建子进程
        pid = os.fork()

        if pid == 0:
            s.close()
            do_child(c,db) #子进程函数
        else:
            c.close()
            t = Thread(target=zombie)
            t.setDaemon(True)
            t.start()
            continue

# 6创建do_child处理函数
def do_child(c,db):
    while True:
        # 接收客户端请求
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == "H":
            do_hist(c,db,data)
def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return
    # 插入用户
    sql = "insert into user (name,passwd) values ('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FAIL')

def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cur = db.cursor()

    sql = "select * from user where name='%s' and passwd='%s'"%(name,passwd)
    cur.execute(sql)
    r = cur.fetchone()
    if r == None:
        c.send(b'FAIL')
    else:
        c.send(b'OK')

def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    # 创建一个内部函数
    def insert_history():
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values ('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback

    # 用单词本查找
    try:
        f = open(DICT_TEXT)
    except:
        c.send(b'FAIL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FAIL')
            f.close()
            return
        elif tmp == word:
            c.send(line.encode())
            insert_history()
            f.close()
            return
    c.send(b'FAIL')
    f.close()

def do_hist(c,db,data):
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = "select * from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'FAIL')
        return
    else:
        c.send(b'OK')
        time.sleep(0.1)
    for i in r:
        msg = "%s   %s   %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')





if __name__ == "__main__":
    main()