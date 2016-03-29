#coding=utf-8
from subprocess import Popen,PIPE
import urllib,urllib2
import re
import subprocess


def get_HostnameInfo(file):
	'''hostname memssage'''
	with open(file,'r') as fd:
		data = fd.read().split('\n')
		for line in data:
			if line.startswith('id'):
				hostname = line.split(':')[1].strip(' ')
				break
	return hostname

def get_Ipaddr():
	'''ipaddr message'''
	P = Popen(['ifconfig'],stdout = PIPE)
	data = P.stdout.read()
	list = []
	str = ''
	option = False
	lines = data.split('\n')
	for line in lines:
		if not line.startswith(' '):
			list.append(str)
			str = line
		else:
			str += line
	while True:
		if '' in list:
			list.remove('')
		else:
			break
	r_devname = re.compile('(eth\d*|em\d*|lo)')
	r_mac = re.compile('HWaddr\s([A-F0-9:]{17})')
	r_ip = re.compile('addr:([\d.]{7,15})')
	for line in list:
		devname = r_devname.findall(line)
		mac = r_mac.findall(line)
		ip = r_ip.findall(line)
		if mac:
			return ip[0]

def get_vir_disk():
	'''get disk info'''
	cmd = "cat /proc/partitions |sed -n '3p' |awk '{print $3}'"
	result = subprocess.os.popen(cmd)
	disk = int(result.read())/1024/1024
	return "".join([str(disk),"G"])

if __name__ == '__main__':
	hostname = get_HostnameInfo('/etc/salt/minion')
	ip = get_Ipaddr()
	vir_disk = get_vir_disk()

	hostinfo = {
	'hostname':hostname,
	'ip':ip,
	'vir_disk':vir_disk,
	'main_host':'node1',
	'location':'G13-1',
	'kvm_location':'\/data\/software\/',
	'host_status':'online'
	}

	data = urllib.urlencode(hostinfo)
	req = urllib2.urlopen('http://10.10.102.13:8000/webkvm/manager_kvm/',data)
	print req.read()
