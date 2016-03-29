#coding=utf-8

from celery import task
import salt.client,os

@task()
def create_vm_linux(hostname,cpus,memory,cloud_name,projects_name,mirror_name,secret_name):
    '''创建linux虚拟机'''
    local = salt.client.LocalClient()
    def find_pub(filepath):
        '''查找公钥'''
        file_list = []
        [file_list.append(i) for i in os.listdir(filepath) if i.endswith('.pub')]
        return file_list
    file_list = find_pub('/data/salt/kvm_manager')
    for i in file_list:
        local.cmd('%s' % hostname,"cp.get_file",['salt://kvm_manager/%s' % i,'/data/software/%s' % i])

    result = local.cmd('%s' % hostname,[
            'cp.get_file',
            'cmd.run',
            'cp.get_file',
            'cp.get_file',
            'cp.get_file',
            'cp.get_file',
            'cmd.run',
        ],
        [
            ['salt://kvm_manager/get_kvm_status.py','/data/software/get_kvm_status.py'],
            ['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
            ['salt://kvm_manager/new_get_kvm_status.py','/data/software/new_get_kvm_status.py'],
            ['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
            ['salt://kvm_manager/centos6_template.xml','/data/software/centos6_template.xml'],
            ['salt://kvm_manager/createtemplate.sh', '/data/software/createtemplate.sh'],
            ['sh /data/software/createtemplate.sh %s %s %s %s %s' % (cpus,memory,cloud_name,mirror_name,secret_name)],
        ])
    return result

@task()
def create_vm_win(hostname,cpus,memory,cloud_name,projects_name,mirror_name):
    '''创建win虚拟机'''
    local = salt.client.LocalClient()
    result = local.cmd('%s' % hostname,[
			'cp.get_file',
			'cmd.run',
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cmd.run',
		],
		[
			['salt://kvm_manager/get_kvm_status.py','/data/software/get_kvm_status.py'],
			['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
			['salt://kvm_manager/new_get_kvm_status_win.py','/data/software/new_get_kvm_status_win.py'],
			['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
			['salt://kvm_manager/centos6_template.xml','/data/software/centos6_template.xml'],
			['salt://kvm_manager/createtemplate_win.sh', '/data/software/createtemplate_win.sh'],
			['sh /data/software/createtemplate_win.sh %s %s %s %s' % (cpus,memory,cloud_name,mirror_name)],
		])

    return result

@task()
def create_vm_xp(hostname,cpus,memory,cloud_name,projects_name,mirror_name):
    '''创建winxp虚拟机'''
    local = salt.client.LocalClient()
    result = local.cmd('%s' % hostname,[
			'cp.get_file',
			'cmd.run',
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cmd.run',
		],
		[
			['salt://kvm_manager/get_kvm_status.py','/data/software/get_kvm_status.py'],
			['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
			['salt://kvm_manager/new_get_kvm_status_win.py','/data/software/new_get_kvm_status_win.py'],
			['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
			['salt://kvm_manager/winxp_template.xml','/data/software/winxp_template.xml'],
			['salt://kvm_manager/createtemplate_xp.sh', '/data/software/createtemplate_xp.sh'],
			['sh /data/software/createtemplate_xp.sh %s %s %s %s' % (cpus,memory,cloud_name,mirror_name)],
		])

    return result


@task()
def create_vm_linux7(hostname,cpus,memory,cloud_name,projects_name, mirror_name):
    '''创建centos7虚拟机'''
    local = salt.client.LocalClient()
    result = local.cmd('%s' % hostname,[
            'cp.get_file',
            'cmd.run',
            'cp.get_file',
            'cp.get_file',
            'cp.get_file',
            'cp.get_file',
            'cmd.run',
        ],
        [
            ['salt://kvm_manager/get_kvm_status.py','/data/software/get_kvm_status.py'],
            ['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
            ['salt://kvm_manager/new_get_kvm_status.py','/data/software/new_get_kvm_status.py'],
            ['salt://kvm_manager/%s.img' % mirror_name,'/data/software/%s.img' % mirror_name],
            ['salt://kvm_manager/centos6_template.xml','/data/software/centos6_template.xml'],
            ['salt://kvm_manager/createtemplate_centos7.sh', '/data/software/createtemplate_centos7.sh'],
            ['sh /data/software/createtemplate_centos7.sh %s %s %s %s' % (cpus,memory,cloud_name,mirror_name)],
        ])
    return result

@task()
def c_snapshot(main_host,hostname):
    '''创建快照'''
    local = salt.client.LocalClient()
    import time
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(now_time,"%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    a = local.cmd("%s" % main_host,"cmd.run",['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap create vm_image/%s.img@%s' % (hostname,timeStamp)])
    return a

@task()
def d_snapshot(main_host,hostname,snapshot_name):
    '''删除快照'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host, "cmd.run",['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap rm vm_image/%s.img@%s' % (hostname,snapshot_name)])
    return a

@task()
def re_snapshot(main_host,hostname,snapshot_name):
    '''从快照还原'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,[
        'cmd.run',
        'cmd.run',
        'cmd.run',
        ],
        [
            ['virsh destroy %s' % hostname],
            ['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap rollback vm_image/%s.img@%s' % (hostname,snapshot_name)],
            ['virsh start %s' % hostname],
        ])
    return a