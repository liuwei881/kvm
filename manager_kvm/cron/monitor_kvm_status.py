#coding=utf-8

import subprocess,MySQLdb,multiprocessing

def ping_status(ip):
	'''检查服务器ping状态'''
	cmd_status = {}
	if subprocess.call('ping -c 1 -W 1 %s > /dev/null' % ip, shell=True) == 0:
		cmd_status[ip] = "online"
	else:
		cmd_status[ip] = "offline"
	return cmd_status
	

    
def get_ip():
	'''获取服务器ip列表'''
	db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","zcloud")
	cursor = db.cursor()
	sql = 'select ip from webkvm_kvm_list;'
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

if __name__ == "__main__":
	ip_list = get_ip()
    
	if len(ip_list) > 30:
		process_number = 30
	else:
		process_number = len(ip_list)
		
	pool = multiprocessing.Pool(processes = process_number)
	result = []
	
	for ip in ip_list:
		r = pool.apply_async(ping_status,(ip,))
		result.append(r)
	pool.close()
	pool.join()
    
	db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","zcloud")
	cursor = db.cursor()
	for i in result:
		state = i.get()
		sql = "update webkvm_kvm_list set host_status = '%s' where ip = '%s'" % (state.values()[0],state.keys()[0])
		if state.values()[0] == "offline":
			try:
				cursor.execute(sql)
				db.commit()
			except Exception,e:
				print e
		elif state.values()[0] == "online":
			try:
				cursor.execute(sql)
				db.commit()
			except Exception,e:
				print e
			
	db.close()
    	
