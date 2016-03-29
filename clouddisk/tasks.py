#coding=utf-8

from celery import task
import salt.client

@task
def mount_disk(main_host,image_name,vm_hostname,ip,dev_name,host_name):
    '''挂载云硬盘'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,
                  [
                      "cp.get_file",
                      "cp.get_file",
                      "cmd.run",
                  ],
                  [
                      ['salt://kvm_manager/mount_image.sh','/data/software/mount_image.sh'],
                      ['salt://kvm_manager/secret.xml','/data/software/secret.xml'],
                      ['sh /data/software/mount_image.sh %s %s %s %s %s' % (image_name,vm_hostname,ip,dev_name,host_name)]

                  ])
    return a

@task
def umount_disk(main_host,vm_hostname,image_name,ip,dev_name):
    '''卸载云硬盘'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,"cmd.run", ['virsh detach-device --persistent %s /etc/libvirt/qemu/disk_%s-%s-%s.xml' % (vm_hostname,image_name,ip,dev_name)])
    return a

@task
def snap_disk(image_name,snap_name):
    '''创建ceph镜像快照'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap create kvms/%s@%s' % (image_name,snap_name)]) #kvms01 为ceph mon 6789的端口
    return a

@task
def del_snap(image_name,snap_name):
    '''删除ceph镜像快照'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap rm kvms/%s@%s' % (image_name,snap_name)])  #kvms01 为ceph mon 6789的端口
    return a

@task
def rollback_snap(image_name,snap_name):
    '''ceph快照回滚'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap rollback kvms/%s@%s' % (image_name,snap_name)])
    return a

@task
def del_image(image_name):
    '''删除ceph镜像'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd rm -p kvms %s' % image_name])
    return a