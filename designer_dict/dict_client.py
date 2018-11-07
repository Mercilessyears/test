#coding=utf8

from socket import *
import sys
import getpass

# 网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
        =================Welcome=================
        ---1.注册         2.登录          3.退出---
        =========================================
        ''')
        try:
            cmd = int(input("请输入命令:"))
        except Exception as e:
            print("命令有错误")
            continue
        
        if cmd not in [1,2,3]:
            print("没有该选项")
            continue
        elif cmd == 1:
            do_register(s)
        elif cmd == 2:
            do_login(s)
        elif cmd == 3:
            s.send(b'E')
            sys.exit("谢谢使用")

def do_register(s):
    while True:
        name = input("User:")
        passwd = getpass.getpass("请输入密码:")
        passwd1 = getpass.getpass("请再次输入密码:")

        if (' ' in name) or (' ' in passwd):
            print("用户名或者密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = 'R %s %s'%(name,passwd)
        s.send(msg.encode())

        # 等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXISTS':
            print('该用户已经存在')
        else:
            print('注册失败')
        return

def do_login(s):
    while True:
        name = input("请输入用户名称:")
        passwd = getpass.getpass('输入密码:')
        if (' ' in name) or (' ' in passwd):
            print('登录失败，请重新输入')
            continue
        msg = 'L %s %s'%(name,passwd)
        s.send(msg.encode())

        data = s.recv(128).decode()
        if data == 'OK':
            print('登录成功')
            # 进入二级界面
            login(s,name)
        else:
            print('登录失败')
        return 

def login(s,name):
    while True:
        print('''
        =================查询界面=================
         1.查询          2.历史记录          3.注销
        =========================================
        ''')
        try:
            cmd = int(input("请输入命令:"))
        except Exception as e:
            print("命令有错误")
            continue
        
        if cmd not in [1,2,3]:
            print("没有该选项")
            continue
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return

def do_query(s,name):
    while True:
        word = input("输入查找单词")
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'FAIL':
            print("没有找到该单词")
        else:
            print(data)

def do_hist(s,name):
    msg = 'H %s'%name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print('没有历史记录')



if __name__ == "__main__":
    main()