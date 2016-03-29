#coding=utf-8

from django.core.management.base import BaseCommand,commandError

class Command(BaseCommand):
    def status(self):
        cmd = "salt-key -L"
        result = subprocess.os.popen(cmd).readlines()
        result1 = result[1:result.index('Denied Keys:\n')]
        status_dic = {}
        for i in result1:
            i = i.strip('\n')
            cmd1 = "salt '%s' cmd.run '%s'" % (i,'virsh list')
            result2 = subprocess.os.popen(cmd1).readlines()
            for i in result2[3:]:
                status_dic[i.split(' ')[9].strip('\n')] = i.split(' ')[-1].strip('\n')

            from django.db import connection,transaction
            cursor = connection.cursor()
            for k,v in status_dic.iteritems():
                if v != 'running':
                    sql = "update webkvm_kvm_list set host_status = '%s' WHERE hostname = '%s'" % ('offline',k)
                    cursor.execute(sql)
                    transaction.set_dirty()
                else:
                    pass
