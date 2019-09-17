"""
chat room　客户端
发送请求，展示结果
"""
from socket import *
import os,sys

#服务器地址
ADDR = ('127.0.0.1',6666)

# 用户发送消息
def send_msg(sockfd,name):
    while True:
        try:
            text = input('>>')
        except (KeyboardInterrupt,SyntaxError):
            text = 'quit'
        if text.strip() == "quit":
            msg = "Q " + name
            sockfd.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        sockfd.sendto(msg.encode(),ADDR)
# 接收消息
def recv_msg(scokfd):
    while True:
        data,addr = sockfd.recvfrom(4096)
        if data.decode() == 'Exit':
            sys.exit()
        print(data.decode()+'\n>>',end='')
# 搭建网络
def main():
    global sockfd
    sockfd = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入您的昵称：")
        msg = 'L '+name
        sockfd.sendto(msg.encode(),ADDR)
        # 接收反馈
        data,addr = sockfd.recvfrom(128)
        if data == b"OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    # 已经进入聊天室
    pid = os.fork()
    if pid < 0:
        sys.exit('Error!')
    elif pid == 0:
        send_msg(sockfd,name)
    else:
        recv_msg(sockfd)


if __name__ == '__main__':
    main()