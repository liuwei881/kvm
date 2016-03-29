#coding=utf-8
import sys
import salt.client
hostname = sys.argv[1]
cpus = sys.argv[2]
memory = sys.argv[3]
cloud_name = sys.argv[4]
projects_name = sys.argv[5]
def create_kvm_win(hostname,cpus,memory,cloud_name,projects_name):
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
			['salt://get_kvm_status.py','/data/software/get_kvm_status.py'],
			['python /data/software/get_kvm_status.py %s %s' % (cloud_name,projects_name)],
			['salt://new_get_kvm_status.py','/data/software/new_get_kvm_status.py'],
			['salt://Win2008r2ent.img','/data/software/Win2008r2ent.img'],
			['salt://centos6_template.xml','/data/software/win_template.xml'],
			['salt://createtemplate_win.sh', '/data/software/createtemplate_win.sh'],
			['sh /data/software/createtemplate_win.sh %s %s %s' % (cpus,memory,cloud_name)],
		])

    return result

if __name__ == "__main__":
    import logging
    logger = logging.getLogger('create_kvm')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/data/createvm_log/create_kvm_win.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    try:
        result_all = create_kvm_win(hostname,cpus,memory,cloud_name,projects_name)
        if result_all == {}:
            logger.debug('create windows vm is ok')
        else:
            logger.debug(result_all)
    except Exception,e:
        logger.debug(e)
