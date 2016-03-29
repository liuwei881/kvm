#coding=utf-8

import subprocess
import multiprocessing,MySQLdb

def ping_status(ip):
	'''检查服务器ping状态'''
	subprocess.call('ping -c 1 -W 1 %s > /dev/null' % ip, shell=True)
	
def ip():
	'''生成ip列表'''
	ip_list = []
	for i in xrange(2,255):
		ip_list.append('10.10.102.%s' % i)
	return ip_list
	
if __name__ == "__main__":
	ip_list = ip()
	if len(ip_list) > 30:
		process_number = 30
	else:
		process_number = len(ip_list)
		
	pool = multiprocessing.Pool(processes = process_number)
	for ip in ip_list:
		pool.apply_async(ping_status,(ip,))
	pool.close()
	pool.join()

	mac = subprocess.os.popen('/sbin/arp')
	m = mac.readlines()
	mac_dict = {}
	for i in m[1:]:
		if i.split('   ')[5] != '':
			mac_dict[i.split('   ')[5]] = i.split('   ')[0]
		
	db = MySQLdb.connect("127.0.0.1","root","QX9rX8UY50gznYo","zcloud")
	cursor = db.cursor()
	sql = 'select mac from webkvm_kvm_list;'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		mac_list = []
		for i in results:
			mac = i[0]
			mac_list.append(mac)
	except Exception,e:
		print 'error'
	for i in mac_list:
		if i in mac_dict.keys():
			sql = "update webkvm_kvm_list set ip = '%s' where mac = '%s' and ip=''" % (mac_dict[i],i)
			try:
				cursor.execute(sql)
				db.commit()
			except Exception,e:
				print e
		else:
			pass		
	db.close()
