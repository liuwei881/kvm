#coding=utf-8

import rrdtool
import time
import MySQLdb
from get_ips import get_ip 

if __name__ == "__main__":
	ip_list = get_ip()
	title = "mem and virtmem info ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

	for i in ip_list:
		rrdtool.graph("../rrddate/images/%s_mem.png" % i,"--start","-1d","--vertical-label=phymem and virtmem(%)","--x-grid",\
			"MINUTE:12:HOUR:1:HOUR:1:0:%H",\
			"--width","550","--height","150","--title",title,\
			"DEF:value1=../rrddate/%s_mem.rrd:phymemusage:AVERAGE" % i,\
			"DEF:value2=../rrddate/%s_mem.rrd:virtmemusage:AVERAGE" % i,\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"AREA:value1#00CC00:phymemusage",\
			"GPRINT:value1:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value1:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value1:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value1:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",\
			"LINE2:value2#FF0033:virtmemusage",\
			"GPRINT:value2:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value2:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value2:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value2:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",
			)
