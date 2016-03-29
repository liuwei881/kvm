#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,diskusage1 from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		diskusage1 = str(float(row[1]))
		update = rrdtool.updatev('../rrddate/%s_disk1.rrd' % ip,'%s:%s' % (starttime,diskusage1))
		print update
except Exception,e:
	print e 
db.close()
