#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,phymemusage,virtmemusage from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		phymemusage = str(float(row[1]))
		virtmemusage = str(float(row[2]))
		update = rrdtool.updatev('../rrddate/%s_mem.rrd' % ip,'%s:%s:%s' % (starttime,phymemusage,virtmemusage))
		print update
except Exception,e:
	print e 
db.close()
