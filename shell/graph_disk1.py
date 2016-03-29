#coding=utf-8

import rrdtool
import time
import MySQLdb
from get_ips import get_ip 

if __name__ == "__main__":
	ip_list = get_ip()
	title = "disk / info ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

	for i in ip_list:
		rrdtool.graph("../rrddate/images/%s_disk1.png" % i,"--start","-1d","--vertical-label=/(%)","--x-grid",\
			"MINUTE:12:HOUR:1:HOUR:1:0:%H",\
			"--width","550","--height","150","--title",title,\
			"DEF:value1=../rrddate/%s_disk1.rrd:diskusage1:AVERAGE" % i,\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"AREA:value1#00CC00:diskusage1",\
			"GPRINT:value1:LAST:'NOW\:%8.0lf'",\
			"GPRINT:value1:AVERAGE:'AVERAGE\:%8.0lf'",\
			"GPRINT:value1:MAX:'MAX\:%8.0lf'",\
			"GPRINT:value1:MIN:'MIN\:%8.0lf'",\
			"COMMENT:\\r",
			)
