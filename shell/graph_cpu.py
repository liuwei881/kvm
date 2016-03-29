#coding=utf-8

import rrdtool
import time
import MySQLdb
from get_ips import get_ip 

if __name__ == "__main__":
	ip_list = get_ip()
	title = "cpu info ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

	for i in ip_list:
		rrdtool.graph("../rrddate/images/%s_cpu.png" % i,"--start","-1d","--vertical-label=%","--x-grid",\
			"MINUTE:12:HOUR:1:HOUR:1:0:%H",\
			"--width","550","--height","150","--title",title,\
			"DEF:value1=../rrddate/%s_cpu.rrd:cpu_user:AVERAGE" % i,\
			"DEF:value2=../rrddate/%s_cpu.rrd:cpu_nice:AVERAGE" % i,\
			"DEF:value3=../rrddate/%s_cpu.rrd:cpu_system:AVERAGE" % i,\
			"DEF:value4=../rrddate/%s_cpu.rrd:cpu_idle:AVERAGE" % i,\
			"DEF:value5=../rrddate/%s_cpu.rrd:cpu_iowait:AVERAGE" % i,\
			"DEF:value6=../rrddate/%s_cpu.rrd:cpu_irq:AVERAGE" % i,\
			"DEF:value7=../rrddate/%s_cpu.rrd:cpu_softirq:AVERAGE" % i,\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"AREA:value1#FF0000:cpu_user",\
			"GPRINT:value1:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value1:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value1:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value1:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value2#8833ff:cpu_nice",\
			"GPRINT:value2:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value2:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value2:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value2:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value3#f7f709:cpu_system",\
			"GPRINT:value3:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value3:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value3:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value3:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value4#00FF00:cpu_idle",\
			"GPRINT:value4:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value4:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value4:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value4:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value5#ff3399:cpu_iowait",\
			"GPRINT:value5:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value5:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value5:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value5:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value6#FF00FF:cpu_irq",\
			"GPRINT:value6:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value6:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value6:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value6:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"AREA:value7#00FFF0:cpu_softirq",\
			"GPRINT:value7:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value7:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value7:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value7:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",
			)
