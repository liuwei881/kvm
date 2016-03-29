#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,diskusage2 from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		diskusage2 = str(float(row[1]))
		update = rrdtool.updatev('../rrddate/%s_disk2.rrd' % ip,'%s:%s' % (starttime,diskusage2))
		print update
except Exception,e:
	print e 
db.close()
