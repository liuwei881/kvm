#coding=utf-8

import salt.client
import json,MySQLdb,datetime

local = salt.client.LocalClient()
a = local.cmd("*","grains.items")
a = json.dumps(a)
h = json.loads(a)
v = []
for i in h.keys():
    location = ""
    sorts = "network"
    salt_status = 'join'
    hostname = h[i]['id'] 
    cpu_num = h[i]['num_cpus']
    cpu_info = h[i]['cpu_model']
    os_info = h[i]['os'] + h[i]['osrelease']
    mem_info = h[i]['Memory']
    create_time = datetime.datetime.now()
    try:
        disk_info = h[i]['disk']
    except Exception,e:
        disk_info = '10G'
    try:
        ip = h[i]['ip4_interfaces']['br0'][0]
    except Exception,e:
        try:
            ip = h[i]['ip4_interfaces']['eth0'][0]
        except Exception,e:
            try:
                ip = h[i]['ip4_interfaces']['p1p1'][0]
            except Exception,e:
                try:
                    ip = h[i]['ip4_interfaces']['enp1s0f0'][0]
                except Exception,e:
                    ip = ''
    try:
        ip1 = h[i]['ip4_interfaces']['eth1'][0]
    except Exception,e:
        try:
            ip1 = h[i]['ip4_interfaces']['p2p1'][0]
        except Exception,e:
            try:
                ip1 = h[i]['ip4_interfaces']['enp1s0f1'][0]
            except Exception,e:
                ip1 = ''
    try:
        ip2 = h[i]['ip4_interfaces']['eth2'][0]
    except Exception,e:
        try:
            ip2 = h[i]['ip4_interfaces']['p3p1'][0]
        except Exception,e:
            try:
                ip2 = h[i]['ip4_interfaces']['eth3'][0]
            except Exception,e:
                ip2 = ''
    t = (hostname,ip,ip1,ip2,location,os_info,mem_info,disk_info,cpu_info,cpu_num,sorts,salt_status,create_time)
    v.append(t)

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","zcloud" )
cursor = db.cursor()
sql = "insert into webkvm_kvmtag(hostname,ip,ip1,ip2,location,osversion,memory,disk,model_name,cpu_core,sorts,salt_status,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
param = tuple(v)
cursor.executemany(sql,param)
cursor.close()
db.commit()
db.close()
