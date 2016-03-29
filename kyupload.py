#coding=utf-8

import paramiko,os,time
from kypform import settings
import random
import base64

def ordianry_ssh(host,username,password,port,cmd):
	password = de_str(settings.SECRET_KEY,str(password))
	s = paramiko.SSHClient()
	s.load_system_host_keys()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(hostname = host,port=int(port),username=username,password=password)
	stdin, stdout, stderr = s.exec_commane(cmd)
	result = stdout.read()
	result = str(result)
	s.close()
	return result

def verification_ssh(host,username,password,port,root_pwd,cmd):
	root_pwd = de_str(str(settings.SECRET_KEY),str(root_pwd))
	password = de_str(str(settings.SECRET_KEY),str(password))
	s = paramiko.SSHClient()
	s.load_system_host_keys()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(hostname = host,username = username,port=int(port),password = password)
	if username != "root":
		ssh = s.invoke_shell()
		time.sleep(0.1)
		ssh.send('su -\n')
		buff = ''
		while not buff.endswith(': ') or buff.endswith('： ')
			resp = ssh.recv(9999)
			buff += resp
		ssh.send(root_pwd)
		ssh.send('\n')
		buff = ''
		while not buff.endswith('# '):
			resp = ssh.recv(9999)
			buff += resp
		ssh.send(cmd)
		ssh.send('\n')
		buff = ''
		while not buff.endswith('# '):
			resp = ssh.recv(9999)
			buff += resp
		s.close()
		result = buff
	else:
		stdin, stdout, stderr = s.exec_command(cmd)
		result = stdout.read()
		result = str(result)
		s.close()
	return result

def upload_run_script(tasklogpath,host,script_list):
	try:
		out = open(tasklogpath,'a')
		script_dir = str(host.script_dir)
		cmd


