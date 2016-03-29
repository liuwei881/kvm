#encoding:utf-8

import psutil,os,subprocess,re,urllib,urllib2

def showcpu():
    cpu_status = psutil.cpu_times_percent()
    cpu_user = cpu_status.user
    cpu_nice = cpu_status.nice
    cpu_system = cpu_status.system
    cpu_idle = cpu_status.idle
    cpu_iowait = cpu_status.iowait
    cpu_irq = cpu_status.irq
    cpu_softirq = cpu_status.softirq         
    return cpu_user, cpu_nice,cpu_system,cpu_idle,cpu_iowait,cpu_irq,cpu_softirq

def showmemory():
    phymemusage=psutil.phymem_usage()
    virtmemusage=psutil.virtmem_usage()
    phymemusage = phymemusage.percent 
    virtmemusage = virtmemusage.percent
    return phymemusage,virtmemusage

def showdisk():
    diskusage1=psutil.disk_usage('/').percent
    diskusage2=psutil.disk_usage('/download').percent
    return diskusage1,diskusage2

def shownet_em():
    netiocounters=psutil.network_io_counters(pernic=True)
    em1_bytes_sent = netiocounters['em1'].bytes_sent
    em1_bytes_recv = netiocounters['em1'].bytes_recv
    em2_bytes_sent = netiocounters['em2'].bytes_sent
    em2_bytes_recv = netiocounters['em2'].bytes_recv
    em3_bytes_sent = netiocounters['em3'].bytes_sent
    em3_bytes_recv = netiocounters['em3'].bytes_recv
    em4_bytes_sent = netiocounters['em4'].bytes_sent
    em4_bytes_recv = netiocounters['em4'].bytes_recv
    return em1_bytes_sent, em1_bytes_recv, em2_bytes_sent, em2_bytes_recv, em3_bytes_sent,em3_bytes_recv, em4_bytes_sent, em4_bytes_recv

def get_cpuload():
    a = os.popen('uptime').read().split(':')[-1].strip('\n').split(',')
    five_load = a[0].strip(' ')
    ten_load = a[1].strip(' ')
    ft_load = a[2].strip(' ')
    return five_load,ten_load,ft_load

def shownet_eth():
    netiocounters=psutil.network_io_counters(pernic=True)
    eth0_bytes_sent = netiocounters['eth0'].bytes_sent
    eth0_bytes_recv = netiocounters['eth0'].bytes_recv
    eth1_bytes_sent = netiocounters['eth1'].bytes_sent
    eth1_bytes_recv = netiocounters['eth1'].bytes_recv
    return eth0_bytes_sent, eth0_bytes_recv, eth1_bytes_sent, eth1_bytes_recv

def get_Ipaddr():
    '''ipaddr message'''
    P = subprocess.Popen('ifconfig',stdout = subprocess.PIPE)
    data = P.stdout.read()
    list = []
    str = ''
    option = False
    lines = data.split('\n')
    for line in lines:
            if not line.startswith(' '):
                    list.append(str)
                    str = line
            else:
                    str += line
    while True:
            if '' in list:
                    list.remove('')
            else:
                    break
    r_devname = re.compile('(eth\d*|em\d*|lo)')
    r_mac = re.compile('HWaddr\s([A-F0-9:]{17})')
    r_ip = re.compile('addr:([\d.]{7,15})')
    for line in list:
            devname = r_devname.findall(line)
            mac = r_mac.findall(line)
            ip = r_ip.findall(line)
            if mac:
                    return ip[0]
        
if __name__=="__main__":
    cpu_user, cpu_nice,cpu_system,cpu_idle,cpu_iowait,cpu_irq,cpu_softirq = showcpu()
    phymemusage,virtmemusage = showmemory()
    diskusage1,diskusage2 = showdisk()
    ip = get_Ipaddr()
    five_load,ten_load,ft_load = get_cpuload()
    
    a = os.popen("ifconfig |grep em |awk '{print $1}' |sed -n 1p").read()
    if "em1" in a:
        em1_bytes_sent, em1_bytes_recv,em2_bytes_sent, em2_bytes_recv, em3_bytes_sent, em3_bytes_recv, em4_bytes_sent, em4_bytes_recv = shownet_em()
        hostinfo = {
            'ip':ip,
            'cpu_user':cpu_user,
            'cpu_nice':cpu_nice,
            'cpu_system':cpu_system,
            'cpu_idle':cpu_idle,
            'cpu_iowait':cpu_iowait,
            'cpu_irq':cpu_irq,
            'cpu_softirq':cpu_softirq,
            'phymemusage':phymemusage,
            'virtmemusage':virtmemusage,
            'diskusage1':diskusage1,
            'diskusage2':diskusage2,
	    'five_load':five_load,
	    'ten_load':ten_load,
            'ft_load':ft_load,
            'em1_bytes_sent':em1_bytes_sent,
            'em1_bytes_recv':em1_bytes_recv,
            'em2_bytes_sent':em2_bytes_sent,
            'em2_bytes_recv':em2_bytes_recv,
            'em3_bytes_sent':em3_bytes_sent,
            'em3_bytes_recv':em3_bytes_recv,
            'em4_bytes_sent':em4_bytes_sent,
            'em4_bytes_recv':em4_bytes_recv
            }  

        data = urllib.urlencode(hostinfo)
        req = urllib2.urlopen('http://117.121.11.25:8000/monitor/',data)
    else:
        eth0_bytes_sent, eth0_bytes_recv, eth1_bytes_sent, eth1_bytes_recv = shownet_eth()
        hostinfo = {
            'ip':ip,
            'cpu_user':cpu_user,
            'cpu_nice':cpu_nice,
            'cpu_system':cpu_system,
            'cpu_idle':cpu_idle,
            'cpu_iowait':cpu_iowait,
            'cpu_irq':cpu_irq,
            'cpu_softirq':cpu_softirq,
            'phymemusage':phymemusage,
            'virtmemusage':virtmemusage,
            'diskusage1':diskusage1,
            'diskusage2':diskusage2,
            'five_load':five_load,
            'ten_load':ten_load,
            'ft_load':ft_load,
            'eth0_bytes_sent':eth0_bytes_sent,
            'eth0_bytes_recv':eth0_bytes_recv,
            'eth1_bytes_sent':eth1_bytes_sent,
            'eth1_bytes_recv':eth1_bytes_recv
            }

        data = urllib.urlencode(hostinfo)
        req = urllib2.urlopen('http://117.121.11.25:8000/monitor/',data)
