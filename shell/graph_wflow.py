#coding=utf-8

import rrdtool
import time
import MySQLdb
from get_ips import get_ip 

if __name__ == "__main__":
	ip_list = get_ip()
	title = "flow info ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

	for i in ip_list:
		rrdtool.graph("../rrddate/images/%s_wflow.png" % i,"--start","-1d","--vertical-label=Bytes/s","--x-grid",\
			"MINUTE:12:HOUR:1:HOUR:1:0:%H",\
			"--width","550","--height","150","--title",title,\
			"DEF:value1=../rrddate/%s_wflow.rrd:em1_bytes_sent:AVERAGE" % i,\
			"DEF:value2=../rrddate/%s_wflow.rrd:em1_bytes_recv:AVERAGE" % i,\
			"CDEF:total_em = value1,value2,+",\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"LINE1:total_em#FF8833:Total traffic",\
			"AREA:value2#00FF00:In traffic",\
			"LINE2:value1#0000FF:Out traffic",\
			"CDEF:inbits_em = value2,8,*",\
			"CDEF:outbits_em = value1,8,*",\
			"COMMENT:\\r",\
			"COMMENT:\\r",\
			"GPRINT:inbits_em:AVERAGE:Avg In traffic\: %6.2lf %Sbps",\
			"COMMENT:   ",\
			"GPRINT:inbits_em:MAX:Max In traffic\: %6.2lf %Sbps",\
			"COMMENT:  ",\
			"GPRINT:inbits_em:MIN:MIN In traffic\: %6.2lf %Sbps\\r",\
			"COMMENT: ",\
			"GPRINT:outbits_em:AVERAGE:Avg Out traffic\: %6.2lf %Sbps",\
			"COMMENT: ",\
			"GPRINT:outbits_em:MAX:Max Out traffic\: %6.2lf %Sbps",\
			"COMMENT: ",\
			"GPRINT:outbits_em:MIN:MIN Out traffic\: %6.2lf %Sbps\\r"
			)
