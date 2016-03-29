#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,em1_bytes_sent,em1_bytes_recv,em2_bytes_sent,em2_bytes_recv,em3_bytes_sent,em3_bytes_recv,em4_bytes_sent,em4_bytes_recv,eth0_bytes_sent,eth0_bytes_recv,eth1_bytes_sent,eth1_bytes_recv from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		em1_bytes_sent = str(row[1])
		em1_bytes_recv = str(row[2])
		em2_bytes_sent = str(row[3])
		em2_bytes_recv = str(row[4])
		em3_bytes_sent = str(row[5])
		em3_bytes_recv = str(row[6])
		em4_bytes_sent = str(row[7])
		em4_bytes_recv = str(row[8])
		eth0_bytes_sent = str(row[9])
		eth0_bytes_recv = str(row[10])
		eth1_bytes_sent = str(row[11])
		eth1_bytes_recv = str(row[12])
		if em1_bytes_sent == 'None':
			em1_bytes_sent = '0'
			em1_bytes_recv = '0'
			em2_bytes_sent = '0'
			em2_bytes_recv = '0'
			update = rrdtool.updatev('../rrddate/%s_wflow.rrd' % ip,'%s:%s:%s:%s:%s' % (starttime,em1_bytes_sent,em1_bytes_recv,eth0_bytes_sent,eth0_bytes_recv))
			update1 = rrdtool.updatev('../rrddate/%s_nflow.rrd' % ip,'%s:%s:%s:%s:%s' % (starttime,em2_bytes_sent,em2_bytes_recv,eth1_bytes_sent,eth1_bytes_recv))
			print update
			print update1
		else:
			eth0_bytes_sent = '0'
			eth0_bytes_recv = '0'
			eth1_bytes_sent = '0'
			eth1_bytes_recv = '0'
			update = rrdtool.updatev('../rrddate/%s_wflow.rrd' % ip,'%s:%s:%s:%s:%s' % (starttime,em1_bytes_sent,em1_bytes_recv,eth0_bytes_sent,eth0_bytes_recv))
			update1 = rrdtool.updatev('../rrddate/%s_nflow.rrd' % ip,'%s:%s:%s:%s:%s' % (starttime,em2_bytes_sent,em2_bytes_recv,eth1_bytes_sent,eth1_bytes_recv))
			print update
			print update1
except Exception,e:
	print e 
db.close()
