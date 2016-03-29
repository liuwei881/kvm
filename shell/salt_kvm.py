#coding=utf-8

import subprocess,sys

kvm_name = sys.argv[1]
vir_name = sys.argv[2]
vir_os = sys.argv[3]
vir_memory = sys.argv[4]
vir_disk = sys.argv[5]
vir_cpu = sys.argv[6]

cmd = "%s %s %s %s %s" % (sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

def salt_kvm(kvm_name, cmd):
	salt_command = 'salt "%s" cmd.run "%s"' % (kvm_name, cmd)
	salt_result = subprocess.os.popen(salt_command)
	print salt_result.read()

if __name__ == "__main__":
	salt_kvm(kvm_name, cmd)
	
