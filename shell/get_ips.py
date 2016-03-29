#coding=utf-8
import MySQLdb

def get_ip():
        '''获取服务器ip地址'''
        db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
        cursor = db.cursor()
        sql='select ip from monitor_host_status;'
        try:
                cursor.execute(sql)
                results = cursor.fetchall()
                ip_list = []
                for row in results:
                        ip = row[0]
                        ip_list.append(ip)
        except Exception,e:
                print "error"
        db.close()
        return ip_list

def get_sent():
	'''获取服务器网卡信息'''
	db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","kypform" )
	cursor = db.cursor()
	sql='select ip, em1_bytes_sent,em1_bytes_recv,em2_bytes_sent,em2_bytes_recv,em3_bytes_sent,em3_bytes_recv,em4_bytes_sent,em4_bytes_recv,eth0_bytes_sent,eth0_bytes_recv,eth1_bytes_sent,eth1_bytes_recv from monitor_host_status;'
	service_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			ip = row[0]
			em1_bytes_sent = row[1]
			em1_bytes_recv = row[2]
			em2_bytes_sent = row[3]
			em2_bytes_recv = row[4]
			em3_bytes_sent = row[5]
			em3_bytes_recv = row[6]
			em4_bytes_sent = row[7]
			em4_bytes_recv = row[8]
			eth0_bytes_sent = row[9]
			eth0_bytes_recv = row[10]
			eth1_bytes_sent = row[11]
			eth1_bytes_recv = row[12]
			service_list.append((ip, em1_bytes_sent,em1_bytes_recv,em2_bytes_sent,em2_bytes_recv,em3_bytes_sent,em3_bytes_recv,em4_bytes_sent,em4_bytes_recv,eth0_bytes_sent,eth0_bytes_recv,eth1_bytes_sent,eth1_bytes_recv))
	except Exception,e:
		print "error"
	db.close()
	return service_list 
