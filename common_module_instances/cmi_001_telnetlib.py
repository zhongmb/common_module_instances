#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
telnetlib
    telnet服务器搭建：win10家庭版，无法开启telnet服务。方案是安装virtualbox虚拟机，虚拟机上安装centos7.2
        centos7安装telnet服务
            1、查看是否安装了相关软件：
                rpm -qa|grep -E "telnet|xinetd"
            显示结果含有以下三个软件，则表示已经安装，否则需要安装缺失的软件
                telnet-server-0.17-60.el7.x86_64
                telnet-0.17-60.el7.x86_64
                xinetd-2.3.15-13.el7.x86_64
            2、安装缺失的软件：
                sudo yum install telnet telnet-server xinetd
            3、注册使用服务：
                sudo systemctl enable telnet.socket
                sudo systemctl start telnet.socket
                sudo systemctl enable xinetd
                sudo systemctl start xinetd
            4、开启防火墙的23端口：
            具体防火墙使用可以参见：http://www.cnblogs.com/moxiaoan/p/5683743.html
                sudo firewall-cmd --zone=public --add-port=23/tcp --permanent
                sudo service firewalld restart
            5、备注：虚拟机如果和主机进行测试，需要将网络模式修改为2. Bridged Adapter，
                具体参见：http://blog.csdn.net/ixidof/article/details/12685549


'''

import sys

def getinput():
    '''获得输入的host,user,passwd信息，并赋予缺省值'''
    import getpass
    host = input("请输入telnet服务器IP地址: ")
    user = input("请输入telnet服务器用户名称: ")
    password = getpass.getpass()
    if not host:
        host = '192.168.1.103'
    if not user:
        user = 'my'
    if not password:
        password = 'my'
    return host, user, password

def test_telnet():
    '''测试telnetlib功能'''
    import telnetlib
    host, user, password = getinput()
    tnl = telnetlib.Telnet(host)
    tnl.read_until(b"login: ")
    tnl.write(user.encode('ascii') + b"\n")
    if password:
        tnl.read_until(b"Password: ")
        tnl.write(password.encode('ascii') + b"\n")
        tnl.write(b"ls\n")
        tnl.write(b"exit\n")
        data = tnl.read_all()
    tnl.close()
    print(data.decode('utf-8'))

def main(argv):
    '''主函数'''
    print("运行参数", argv)
    print(__doc__)
    test_telnet()


if __name__ == "__main__":
    main(sys.argv)
