#coding=utf-8

import paramiko,sys 

hostname = sys.argv[1]
username = sys.argv[2]
port = sys.argv[3]
cmd = sys.argv[4]
def runcmd(hostname,username,port,cmd):
	pkey='/root/.ssh/id_rsa'
	key=paramiko.RSAKey.from_private_key_file(pkey)
	ssh = paramiko.SSHClient()  
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=hostname,username = username,pkey=key,port=int(port))
	stdin,stdout,stderr=ssh.exec_command(cmd) 
	print stdout.read() 

if __name__ == "__main__":
	runcmd(hostname,username,port,cmd)
