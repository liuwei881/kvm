#coding=utf-8

import subprocess,sys

hostname = sys.argv[1]
cmd = sys.argv[2]
def salt_cmd(hostname, cmd):
	salt_command = 'salt "%s" cmd.run "%s"' % (hostname, cmd)
	salt_result = subprocess.os.popen(salt_command)
	print salt_result.read()

if __name__ == "__main__":
	salt_cmd(hostname, cmd)
	
