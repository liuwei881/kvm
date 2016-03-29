#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,five_load,ten_load,ft_load from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		five_load = str(float(row[1]))
		ten_load = str(float(row[2]))
		ft_load = str(float(row[3]))
		update = rrdtool.updatev('../rrddate/%s_load.rrd' % ip,'%s:%s:%s:%s' % (starttime,five_load,ten_load,ft_load))
		print update
except Exception,e:
	print e 
db.close()
