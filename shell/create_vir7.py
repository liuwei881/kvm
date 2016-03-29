#coding=utf-8

import salt.client
import sys
hostname = sys.argv[1]
cpus = sys.argv[2]
memory = sys.argv[3]
cloud_name = sys.argv[4]
projects_name = sys.argv[5]
def create_kvm_linux(hostname,cpus,memory,cloud_name,projects_name):
    '''创建linux虚拟机'''
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
            ['salt://get_kvm_status.py','/data/software/get_kvm_status.py'],
            ['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
            ['salt://new_get_kvm_status.py','/data/software/new_get_kvm_status.py'],
            ['salt://centos7.img','/data/software/centos7.img'],
            ['salt://centos6_template.xml','/data/software/centos6_template.xml'],
            ['salt://createtemplate_centos7.sh', '/data/software/createtemplate_centos7.sh'],
            ['sh /data/software/createtemplate_centos7.sh %s %s %s' % (cpus,memory,cloud_name)],
        ])
    return result

if __name__ == "__main__":
    import logging
    logger = logging.getLogger('create_kvm')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/data/createvm_log/create_kvm_linux.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    try:
        result_all = create_kvm_linux(hostname,cpus,memory,cloud_name,projects_name)
        if result_all == {}:
            logger.debug('create centos7 vm is ok')
        else:
            logger.debug(result_all)
    except Exception,e:
        logger.debug(e)
