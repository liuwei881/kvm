#!coding=utf-8

import MySQLdb
import rrdtool,time

db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
cursor = db.cursor()
sql='select ip,cpu_user,cpu_nice,cpu_system,cpu_idle,cpu_iowait,cpu_irq,cpu_softirq from monitor_host_status;'
starttime=str(int(time.time()))
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		ip = row[0]
		cpu_user = str(float(row[1]))
		cpu_nice = str(float(row[2]))
		cpu_system = str(float(row[3]))
		cpu_idle = str(float(row[4]))
		cpu_iowait = str(float(row[5]))
		cpu_irq = str(float(row[6]))
		cpu_softirq = str(float(row[7]))
		update = rrdtool.updatev('../rrddate/%s_cpu.rrd' % ip,'%s:%s:%s:%s:%s:%s:%s:%s' % (starttime,cpu_user,cpu_nice,cpu_system,cpu_idle,cpu_iowait,cpu_irq,cpu_softirq))
		print update
except Exception,e:
	print e 
db.close()
