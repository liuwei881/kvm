#coding=utf-8

import rrdtool
import time
import MySQLdb
from get_ips import get_ip 

if __name__ == "__main__":
	ip_list = get_ip()
	title = "cpu_load info ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

	for i in ip_list:
		rrdtool.graph("../rrddate/images/%s_load.png" % i,"--start","-1d","--vertical-label=cpu processor","--x-grid",\
			"MINUTE:12:HOUR:1:HOUR:1:0:%H",\
			"--width","550","--height","150","--title",title,\
			"DEF:value1=../rrddate/%s_load.rrd:five_load:AVERAGE" % i,\
			"DEF:value2=../rrddate/%s_load.rrd:ten_load:AVERAGE" % i,\
			"DEF:value3=../rrddate/%s_load.rrd:ft_load:AVERAGE" % i,\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"LINE1:value1#339900:five_load",\
			"GPRINT:value1:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value1:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value1:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value1:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"LINE2:value2#0000FF:ten_load",\
			"GPRINT:value2:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value2:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value2:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value2:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"LINE3:value3#FF0000:ft_load",\
			"GPRINT:value3:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value3:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value3:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value3:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",
			)
