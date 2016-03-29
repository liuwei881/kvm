#coding=utf-8

import rrdtool
import time
import MySQLdb
import os
from get_ips import get_sent,get_ip

cur_time = str(int(time.time()))

if __name__ == "__main__":
	ip_list = get_ip()
	for i in ip_list:
		rrd = rrdtool.create('../rrddate/%s_nflow.rrd' % i,'--step','600','--start',cur_time,
			'DS:em2_in:COUNTER:800:0:U',
			'DS:em2_out:COUNTER:800:0:U',
			'DS:eth1_in:COUNTER:800:0:U',
			'DS:eth1_out:COUNTER:800:0:U',
			'RRA:AVERAGE:0.5:1:600',
			'RRA:AVERAGE:0.5:6:700',
			'RRA:AVERAGE:0.5:24:775',
			'RRA:AVERAGE:0.5:288:797',
			'RRA:MAX:0.5:1:600',
			'RRA:MAX:0.5:6:700',
			'RRA:MAX:0.5:24:775',
			'RRA:MAX:0.5:444:797',
			'RRA:MIN:0.5:1:600',
			'RRA:MIN:0.5:6:700',
			'RRA:MIN:0.5:24:775',
			'RRA:MIN:0.5:444:797')

		if rrd:
			print rrdtool.error()
