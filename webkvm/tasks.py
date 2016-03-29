#coding=utf-8

from celery import task
import salt.client,subprocess

@task()
def start_vm(main_host, vir_name):
    '''启动虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,"virt.start",[vir_name])
    return a

@task()
def stop_vm(main_host, vir_name):
    '''关闭虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,"virt.stop",[vir_name])
    return a

@task()
def reboot_vm(main_host, vir_name):
    '''重启虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,
                  [
                      "virt.stop",
                      "virt.start",
                  ],
                  [
                    [vir_name],
                    [vir_name]
                  ])
    return a

@task()
def vm_del(main_host, hostname):
    '''删除虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,
                [
                    "virt.stop",
                    "virt.undefine",
                    "cmd.run",
                ],
                [
                    [hostname],
                    [hostname],
                    ['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 rm vm_image/%s.img' % hostname]
                ])
    return a

@task()
def createkey(keyname):
    '''创建密钥对'''
    a = subprocess.call("ssh-keygen -f /root/.ssh/%s -P '' && mv /root/.ssh/%s /data/py/zxrCloud/keypairs/download/ && chmod 644 /data/py/zxrCloud/keypairs/download/%s && mv /root/.ssh/%s.pub /data/salt/kvm_manager" % (keyname,keyname,keyname,keyname),shell=True)
    return a

@task()
def delkey(keyname):
    '''删除密钥对'''
    a = subprocess.call('rm /data/salt/kvm_manager/%s -rf && rm /data/py/zxrCloud/keypairs/download/%s -rf' % (keyname,keyname),shell=True)
    return a
