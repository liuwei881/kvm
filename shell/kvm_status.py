#coding=utf-8

import subprocess,urllib,urllib2

cmd_status = {}
def ping_status(ip_list):
    '''检查服务器ping状态'''
    for ip in ip_list:
        ping_cmd = "ping -c 3 %s" % ip
        cmd = subprocess.os.popen(ping_cmd)
        cmd_result = cmd.readlines()[-2].split(',')[1].strip(' ').split(' ')[0]
        if cmd_result == '3':
            cmd_status[ip] = 'online'
        else:
            cmd_status[ip] = 'offline'
    return cmd_status


if __name__ == "__main__":
    ip_list = ('10.10.102.13','10.10.102.14','10.10.102.15','10.10.102.17')
    host_dic = ping_status(ip_list)
    for k,v in host_dic.iteritems():
        hostinfo = {
            'ip':k,
            'host_status':v
        }

        data = urllib.urlencode(hostinfo)
        req = urllib2.urlopen('http://10.10.102.13:8000/webkvm/manager_kvm/',data)
        print req.read()
