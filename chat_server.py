"""
chat room 服务端
env: ptyhon3.6
socket udp & fork
"""
from socket import *
import os

# 全局变量：很多封装模块都要用，或者有特定含义的变量
HOST = '0.0.0.0'
PORT = 6666
ADDR = (HOST,PORT)

# 存储用户　{name:address}
USER = {}

#处理用户登录
def do_login(sockfd,name,addr):
    if name in USER or '管理员' in name:
        sockfd.sendto('用户名已存在'.encode(),addr)
        return
    else:
        sockfd.sendto(b'OK',addr)
    msg = "\n欢迎 %s 加入群聊" %name
    for i in USER:
        sockfd.sendto(msg.encode(),USER[i])
    USER[name] = addr
# 处理聊天
def do_chat(sockfd,name,text):
    msg = '\n%s : %s' %(name,text)
    for i in USER:
        #不发送给自己
        if i != name:
            sockfd.sendto(msg.encode(),USER[i])
# 处理退出
def do_exit(sockfd,name):
    msg = "\n%s 已退出群聊" %name
    for i in USER:
        if i != name:
            sockfd.sendto(msg.encode(),USER[i])
        else:
            sockfd.sendto(b"Exit",USER[i])
    del USER[name] #删除推出的用户

# 循环接收用户端请求
def do_request(sockfd):
    while True:
        data,addr = sockfd.recvfrom(1024)
        # if data.decode().split(' ')[0] == 'L':
        tmp = data.decode().split(' ',2) #只切前两个空格
        # 根据不同的请求类型，执行不同的事件
        if tmp[0] == 'L':
            do_login(sockfd,tmp[1],addr)
        elif tmp[0] == "C":
            do_chat(sockfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            do_exit(sockfd,tmp[1])

#搭建网络
def main():
    #udp网络
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)
    pid = os.fork()
    if pid == 0:
        # 管理员消息处理
        while True:
            text = input("管理员消息：")
            msg = "C 管理员 " + text
            sockfd.sendto(msg.encode(),ADDR)
    else:
        do_request(sockfd) # 接收客户端请求

if __name__ == '__main__':
    main()