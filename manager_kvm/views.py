#coding=utf-8
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from webkvm.models import kvm_list,mirrorname,secret_key
import json,subprocess,datetime
import salt.client
import random
from manager_kvm.models import snapshot_show
from pro_manage.models import projects,pro_user_relation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def addHost_kvm(request):
    '''创建kvm虚拟机'''
    local = salt.client.LocalClient()
    host_status = local.cmd("computer[1-6,11]*-112-*.iprun.com","grains.item", ["freemem"])     #freemem为自己定义
    h = random.choice(host_status.items())
    memory = int(h[1].values()[0].strip("G").split(".")[0])
    if memory <= 3:
        return HttpResponse(json.dumps({'status':200,'msg':'此台服务器内存已满，请重新创建'}), content_type="application/json")
    else:
        hostname = h[0]
        try:
            if 'cloud_name' in request.GET and request.GET["cloud_name"]:
                cloud_name = request.GET['cloud_name']
                cpus = request.GET['cpus']
                system = request.GET['system']
                mirror_name = request.GET['mirror_name']
                projects_name = request.GET['projects_name']
                sename = secret_key.objects.filter(projects_name = projects_name)
                secret_name = []
                [secret_name.append(i.secretkey_name) for i in sename]
                secret_name = ",".join(secret_name)
                cpu = str(cpus)
                cpus = cpu.split("_")[0][0]
                memory = int(cpu.split("_")[1][0]) * 1024 * 1024
                proname = projects.objects.get(pro_name = projects_name)
                c_cpu = proname.c_cpu
                c_memory = proname.c_memory
                c_projects = kvm_list.objects.filter(projects_name = projects_name)
                c_config = c_projects.count() + 1
                v = []
                [v.append(i.vir_disk) for i in c_projects]
                v_cpu = []
                v_memory = []
                [v_cpu.append(int(i.split('_')[0][0])) or v_memory.append(int(i.split('_')[1][0])) for i in v]
                now_cpu = sum(v_cpu) + int(cpus)
                now_memory = sum(v_memory) + int(cpu.split("_")[1][0])
                if now_cpu < c_cpu and now_memory < c_memory:
                    from tasks import create_vm_linux,create_vm_win,create_vm_xp
                    if system == '2' and mirror_name == mirrorname.objects.get(mirror_name = mirror_name).mirror_name:
                        subprocess.call('sh /data/salt/kvm_manager/create_temp.sh %s' % hostname, shell=True)
                        create_vm_linux.delay(hostname,cpus,memory,cloud_name,projects_name,mirror_name,secret_name)
                        projects.objects.filter(pro_name = projects_name).update(v_cpu = now_cpu,v_memory= now_memory,c_config = c_config)
                        return HttpResponse(json.dumps({'status':200,'msg':'正在创建kvm,请移步到虚拟机管理查看'}), content_type="application/json")
                    elif mirror_name == 'winxp':
                        subprocess.call('sh /data/salt/kvm_manager/create_temp2.sh %s' % hostname, shell=True)
                        create_vm_xp.delay(hostname,cpus,memory,cloud_name,projects_name,mirror_name)
                        projects.objects.filter(pro_name = projects_name).update(v_cpu = now_cpu,v_memory= now_memory,c_config = c_config)
                        return HttpResponse(json.dumps({'status':200,'msg':'正在创建kvm,请移步到虚拟机管理查看'}), content_type="application/json")
                    else:
                        subprocess.call('sh /data/salt/kvm_manager/create_temp.sh %s' % hostname, shell=True)
                        create_vm_win.delay(hostname,cpus,memory,cloud_name,projects_name,mirror_name)
                        projects.objects.filter(pro_name = projects_name).update(v_cpu = now_cpu,v_memory= now_memory,c_config = c_config)
                        return HttpResponse(json.dumps({'status':200,'msg':'正在创建kvm,请移步到虚拟机管理查看'}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status':200,'msg':'虚拟机超过配额，请联系管理员增加配额'}), content_type="application/json")
            else:
                return HttpResponseRedirect('/webkvm/')
        except Exception,e:
            return HttpResponseRedirect('/webkvm/')

@login_required
def shutdown_Host(request):
    '''准备关闭所有宿主机'''
    username = request.session.get('username')
    return render_to_response('manager_kvm/shutdown_Host.html',{'username':username})

@login_required
def shutdown_all(request):
    '''关闭所有宿主机'''
    local = salt.client.LocalClient()
    local.cmd("*", "cmd.run",['init 0'])
    return HttpResponseRedirect('/webkvm/')

@login_required
def snapshot(request):
    '''kvm快照管理'''
    h = kvm_list.objects.all()
    username = request.session.get('username')
    return render_to_response('manager_kvm/snapshot.html',{'h':h,'username':username})

@login_required
def snapshot_create(request,id):
    '''创建快照'''
    h = kvm_list.objects.get(id = id)
    hostname = h.hostname
    main_host = h.main_host
    from tasks import c_snapshot
    c_snapshot.delay(main_host,hostname)
    import time
    time.sleep(1)
    local = salt.client.LocalClient()
    result = local.cmd("%s" % main_host, "cmd.run",['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap ls vm_image/%s.img' % hostname])
    try:
        result_list = result.values()[0].split(' ')
        snapshot_name = result_list[-3]
        create_time = datetime.datetime.now()
        s = snapshot_show.objects.filter(snapshot_name = snapshot_name)
        if list(s) == []:
            snapshot_show(hostname_id = id,
                        s_hostname = hostname,
                        snapshot_name = snapshot_name,
                        create_time = create_time,
                        snapshot_num = 1,
                        auto_create = 'no'
                        ).save()
        else:
            s.update(hostname_id = id,
                     s_hostname = hostname,
                     snapshot_name = snapshot_name,
                     snapshot_num = 1
                     )
    except Exception,e:
        username = request.session.get('username')
        render_to_response("manager_kvm/error_snapshot.html",{'h':h,'username':username})
    snap = snapshot_show.objects.filter(hostname_id = id)
    all_list = snap.values_list()
    s_dic = {}
    for k in xrange(len(all_list)):
        s_dic[k] = all_list[k][3]
    for k,v in s_dic.iteritems():
        snapshot_show.objects.filter(snapshot_name = v).update(snapshot_num = k)
    return HttpResponseRedirect("/webkvm/manager_kvm/")

@login_required
def show_snapshot(request, id):
    '''查看快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvm_list.objects.get(id = id)
    all_snap = snapshot_show.objects.all()
    if username != 'admin':
        user = User.objects.get(username = username)
        user_id = user.id
        items = pro_user_relation.objects.filter(user_id = user_id)
        id_list = []
        for i in items:
            id_list.append(i.project_id)
        pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
        pro = h.projects_name
        pro = projects.objects.get(pro_name = pro)
        return render_to_response("manager_kvm/show_snapshot.html", locals())
    return render_to_response("manager_kvm/show_snapshot.html", locals())

@login_required
def del_snapshot(request, id, k):
    '''删除快照'''
    h = kvm_list.objects.get(id = id)
    hostname = h.hostname
    main_host = h.main_host
    all_snap = snapshot_show.objects.all()
    try:
        snap = snapshot_show.objects.filter(hostname_id = id,snapshot_num = k)
        all_list = snap.values_list()
        snapshot_name = all_list[0][3]
    except Exception,e:
        username = request.session.get('username')
        return render_to_response("manager_kvm/show_snapshot.html",{'h':h,'all_snap':all_snap,'username':username})
    from tasks import d_snapshot
    d_snapshot.delay(main_host,hostname,snapshot_name)
    snapshot_show.objects.filter(snapshot_name = snapshot_name).delete()
    username = request.session.get('username')
    return render_to_response("manager_kvm/show_snapshot.html",{'h':h,'all_snap':all_snap,'username':username})

@login_required
def re_snapshot(request, id, k):
    '''从快照中恢复虚拟机'''
    username = request.session.get('username')
    h = kvm_list.objects.get(id = id)
    hostname = h.hostname
    main_host = h.main_host
    snap = snapshot_show.objects.filter(hostname_id = id)
    all_list = snap.values_list()
    try:
        s_dic = {}
        for k in xrange(len(all_list)):
            s_dic[k] = all_list[k][3]
        snapshot_name = s_dic[k]
        from tasks import re_snapshot
        re_snapshot.delay(main_host,hostname,snapshot_name)
    except Exception,e:
        return render_to_response("manager_kvm/error_re_snapshot.html",{'username':username})
    return render_to_response("manager_kvm/re_snapshot.html",{'username':username})

@login_required
def show_cloudname(request, id):
    '''显示要修改的云主机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvm_list.objects.get(id = id)
    user = User.objects.get(username = username)
    user_id = user.id
    items = pro_user_relation.objects.filter(user_id = user_id)
    id_list = []
    for i in items:
        id_list.append(i.project_id)
    pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
    pro = h.projects_name
    pro = projects.objects.get(pro_name = pro)
    return render_to_response('manager_kvm/edit_yunname.html',locals())

@login_required
def editname(request, id):
    '''修改云主机名称'''
    h = kvm_list.objects.get(id = id)
    try:
        if 'cloud_name' in request.GET and request.GET["cloud_name"]:
            cloud_name = request.GET["cloud_name"]
            kvm_list.objects.filter(ip = h.ip).update(cloud_name = cloud_name)
        else:
            print "ok"
    except Exception,e:
        return HttpResponseRedirect('/webkvm/manager_kvm/')
    return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def vnc_start(request,id):
    '''启动vnc'''
    h = kvm_list.objects.get(id = id)
    hostname = h.hostname
    html = "http://10.10.112.10:8000/vnc_auto.html?path=websockify/?token=%s" % hostname
    return redirect(html)

def get_system(request):
    '''获取操作系统'''
    if request.method == 'POST':
        try:
            parent = int(request.POST['parent'])
            level = int(request.POST['level'])
            system = mirrorname.objects.filter(parent=parent,level=level)
            dict_system = []
            for i in system:
                temp = []
                temp.append(i.id)
                temp.append(i.mirror_name)
                dict_system.append(temp)
            return HttpResponse(json.dumps({"dict_system":dict_system}))
        except Exception,e:
            return HttpResponse(e)
    else:
        pass
