#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from webkvm.models import kvmtag,kvm_list,secret_key,zcloud_size,mirror_size
from pro_manage.models import projects,pro_user_relation
import subprocess,json,datetime
from tasks import start_vm,stop_vm,reboot_vm,vm_del
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def servers_webkvm(request):
    '''kvm宿主机'''
    username = request.session.get('username')
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        ip1 = request.POST.get('ip1')
        ip2 = request.POST.get('ip2')
        location = request.POST.get('location')
        osversion = request.POST.get('osversion')
        memory = request.POST.get('memory')
        disk = request.POST.get('disk')
        model_name = request.POST.get('model_name')
        cpu_core = request.POST.get('cpu_core')
        sorts = request.POST.get('sorts')
        salt_status = request.POST.get('salt_status')

        host = kvmtag.objects.filter(ip = ip)
        try:
            if list(host) == []:
                host = kvmtag
                h = host(hostname = hostname,
                        ip = ip,
                        ip1 = ip1,
                        ip2 = ip2,
                        location = location,
                        osversion = osversion,
                        memory = memory,
                        disk = disk,
                        model_name = model_name,
                        cpu_core = cpu_core,
                        sorts = sorts,
                        salt_status = salt_status
                        )
                h.save()
            else:
                host.update(hostname = hostname,
                            ip = ip,
                            ip1 = ip1,
                            ip2 = ip2,
                            location = location,
                            osversion = osversion,
                            memory = memory,
                            disk = disk,
                            model_name = model_name,
                            cpu_core = cpu_core,
                            sorts = sorts,
                            salt_status = salt_status
                            )
                return HttpResponse("ok")
        except Exception,e:
            print e
    else:
        List = kvmtag.objects.order_by('-id')
        paginator = Paginator(List, 10)
        pro_projects = projects.objects.all()
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            List = paginator.page(page)
        except (EmptyPage, InvalidPage):
            List = paginator.page(paginator.num_pages)
        return render_to_response('webkvm/servers_webkvm.html', {'List':List,'paginator':paginator,'pro_projects':pro_projects,'username':username})

@login_required
def manager_Host(request, id):
    '''管理kvm宿主机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvmtag.objects.get(id = id)
    return render_to_response('webkvm/manager_Host.html', {'h':h,'username':username})

def join_salt(request, id):
    '''手动添加salt客户端'''
    h = kvmtag.objects.get(id = id)
    cmd1 = "salt-key -L"
    result1 = subprocess.os.popen(cmd1).readlines()
    new_result = []        
    for i in result1[1:result1.index('Denied Keys:\n')]:
        i = i.strip('\n')
        new_result.append(i)

    if h.hostname not in new_result:
        cmd = "salt-key -a %s -y" % (h.hostname)
        subprocess.os.popen(cmd)
        salt_status = 'join'
        host = kvmtag.objects.filter(ip = h.ip)
        host.update(hostname = h.hostname,
                    ip = h.ip,
                    location = h.location,
                    osversion = h.osversion,
                    memory = h.memory,
                    disk = h.disk,
                    model_name = h.model_name,
                    cpu_core = h.cpu_core,
                    salt_status = salt_status
                    )
        return HttpResponseRedirect('/webkvm/')
    else:
        return HttpResponseRedirect('/webkvm/')

@login_required
def show_host(request, id):
    '''显示kvm宿主机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvmtag.objects.get(id = id)
    return render_to_response('webkvm/edit_host.html', {'h':h,'username':username})

@login_required
def edit_host(request, id):
    '''编辑kvm宿主机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvmtag.objects.get(id = id)
    try:
        if 'location' in request.GET and request.GET["location"]:
            location = request.GET["location"]
            Sort = request.GET["Sort"]
            kvmtag.objects.filter(hostname = h.hostname).update(location = location,sorts = Sort)
        else:
            print "ok"
    except Exception,e:
        return HttpResponseRedirect('/webkvm/')
    return HttpResponseRedirect('/webkvm/')

@login_required
def search_kvm(reqeust,id):
    '''查询虚拟机'''
    username = reqeust.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    query = reqeust.GET.get('q','')
    if query:
        qset = (
            Q(cloud_name__icontains = query)|
            Q(main_host__icontains = query)|
            Q(ip__icontains = query)|
            Q(hostname__icontains = query)|
            Q(projects_name__icontains = query)
        )
        user = User.objects.get(username = username)
        user_id = user.id
        items = pro_user_relation.objects.filter(user_id = user_id)
        id_list = []
        for i in items:
            id_list.append(i.project_id)
        pro_projects = projects.objects.filter(pk__in = id_list)
        pro = projects.objects.get(id = id)
        results = kvm_list.objects.filter(qset,projects_name = pro.pro_name)
        return render_to_response("webkvm/search_result.html",locals())
    else:
        results = []
        return render_to_response("webkvm/search_result.html",locals())

@login_required
def search_kvm2(reqeust):
    '''特供admin用户查询'''
    username = reqeust.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    query = reqeust.GET.get('q','')
    if query:
        qset = (
            Q(cloud_name__icontains = query)|
            Q(main_host__icontains = query)|
            Q(ip__icontains = query)|
            Q(hostname__icontains = query)|
            Q(projects_name__icontains = query)
        )
        results = kvm_list.objects.filter(qset)
        pro_projects = projects.objects.all()
        return render_to_response("webkvm/search_result.html",locals())
    else:
        results = []
        return render_to_response("webkvm/search_result.html",locals())

def search_projects(request):
    '''查询项目名称'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if username == 'admin':
        pro_projects = projects.objects.all()
        query = request.GET.get('projects','')
        if query:
            qset = (
                Q(projects_name__icontains = query)
            )
            results = kvm_list.objects.filter(qset)
        else:
            results = []
        return render_to_response("webkvm/search_projects.html",{"results":results,"pro_projects":pro_projects,"username":username})
    else:
        user = User.objects.get(username = username)
        user_id = user.id
        items = pro_user_relation.objects.filter(user_id = user_id)
        id_list = []
        for i in items:
            id_list.append(i.project_id)
        pro_projects = projects.objects.filter(pk__in = id_list)
        query = request.GET.get('projects','')
        if query:
            qset = (
                Q(projects_name__icontains = query)
            )
            results = kvm_list.objects.filter(qset)
        else:
            results = []
        return render_to_response("webkvm/search_projects.html",{"results":results,"pro_projects":pro_projects,"username":username})

def manager_kvm(request):
    '''kvm虚拟机配置'''
    if request.method == 'POST':
        cloud_name = request.POST.get('cloud_name')
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        vir_disk = request.POST.get('vir_disk')
        main_host = request.POST.get('main_host')
        location = request.POST.get('location')
        kvm_location = request.POST.get('kvm_location')
        create_time = request.POST.get('create_time')
        projects_name = request.POST.get('projects_name')
        mac = request.POST.get('mac')
        host_status = request.POST.get('host_status')
        mirror_name = request.POST.get('mirror_name')
        secret_name = request.POST.get('secret_name')
        #try:
            #pro = projects.objects.get(pro_name = projects_name)
            #projects_name = pro.projects_name
        #except Exception,e:
        #    projects_name = "未定义"
        try:
            if hostname !="" and mac !="":
                kvm_list.objects.filter(hostname ="",ip="").update(
                    cloud_name = cloud_name,
                    hostname = hostname,
                    ip = ip,
                    mac = mac,
                    vir_disk = vir_disk,
                    main_host = main_host,
                    location = location,
                    kvm_location = kvm_location,
                    host_status=host_status,
                    mirror_name = mirror_name,
                    secret_name = secret_name
                )
            else:
                kvm_list(
                    cloud_name = cloud_name,
                    hostname = hostname,
                    ip = ip,
                    vir_disk = vir_disk,
                    main_host = main_host,
                    location = location,
                    kvm_location = kvm_location,
                    projects_name = projects_name,
                    mac = mac,
                    create_time = create_time,
                    host_status = host_status
                ).save()
        except Exception,e:
            return HttpResponse(json.dumps({'msg':'更新状态有错误','错误':e}), content_type="application/json")
    else:
        username = request.session.get('username')
        if username == None:
            return HttpResponseRedirect('/login/')
        List = kvm_list.objects.order_by('-id')
        paginator = Paginator(List, 15)
        pro_projects = projects.objects.order_by('id').all()
        pro = pro_projects[0]
        keys = secret_key.objects.all()
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        try:
            List = paginator.page(page)
        except (EmptyPage, InvalidPage):
            List = paginator.page(paginator.num_pages)
        if username != 'admin':
            user = User.objects.get(username = username)
            user_id = user.id
            items = pro_user_relation.objects.filter(user_id = user_id)
            id_list = []
            for i in items:
                id_list.append(i.project_id)
            pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
            pro = pro_projects[0]
            pro_name = []
            for i in pro_projects:
                pro_name.append(i.pro_name)
            List = kvm_list.objects.order_by('-id').filter(projects_name__in = pro_name )
            paginator = Paginator(List, 15)
            try:
                page = int(request.GET.get('page','1'))
            except ValueError:
                page = 1
            try:
                List = paginator.page(page)
            except (EmptyPage, InvalidPage):
                List = paginator.page(paginator.num_pages)
            return render_to_response('webkvm/manager_kvm.html',
                                      {'List':List,
                                       'paginator':paginator,
                                       'pro_projects':pro_projects,
                                       'username':username,
                                       'keys':keys,
                                       'pro':pro
                                        }
                                      )
        else:
            return render_to_response('webkvm/manager_kvm.html',
                                      {'List':List,
                                       'paginator':paginator,
                                       'pro_projects':pro_projects,
                                       'username':username,
                                       'keys':keys,
                                       'pro':pro
                                       }
                                      )

@login_required
def start(request, id):
    '''启动kvm虚拟机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvm_list.objects.get(id = id)
    main_host = h.main_host
    vir_name = h.hostname
    start_vm.delay(main_host,vir_name)
    return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def shutdown(request, id):
    '''关闭kvm虚拟机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvm_list.objects.get(id = id)
    main_host = h.main_host
    vir_name = h.hostname
    stop_vm.delay(main_host,vir_name)
    return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def reboot(request, id):
    '''重启kvm虚拟机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = kvm_list.objects.get(id = id)
    main_host = h.main_host
    vir_name = h.hostname
    reboot_vm.delay(main_host,vir_name)
    return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def del_vm(request, id):
    '''删除kvm虚拟机'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        h = kvm_list.objects.get(id = id)
        hostname = h.hostname
        main_host = h.main_host
        vir_disk = h.vir_disk
        vm_del.delay(main_host, hostname)
        projects_name = h.projects_name
        h_cpu = int(vir_disk.split("_")[0][0])
        h_mem = int(vir_disk.split("_")[1][0])
        p = projects.objects.get(pro_name = projects_name)
        c_config = int(p.c_config) - 1
        v_cpu = p.v_cpu - h_cpu
        v_mem = p.v_memory - h_mem
        if v_cpu < 0:
            v_cpu = 0
        elif v_mem < 0:
            v_mem = 0
        projects.objects.filter(pro_name = projects_name).update(v_cpu = v_cpu,v_memory = v_mem,c_config = c_config)
        kvm_list.objects.filter(hostname = hostname).delete()
        subprocess.call('cat /data/software/vnc/vnc_tokens |grep %s |xargs -i sed -i "s/{}//g" /data/software/vnc/vnc_tokens' % hostname, shell=True)
    except Exception,e:
        return HttpResponseRedirect('/webkvm/manager_kvm/')
    return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def show_key(request,id):
    '''查看密钥对'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    user = User.objects.get(username = username)
    user_id = user.id
    items = pro_user_relation.objects.filter(user_id = user_id)
    id_list = []
    for i in items:
        id_list.append(i.project_id)
    pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
    pro = projects.objects.get(id = id)
    pro_name = []
    for i in pro_projects:
        pro_name.append(i.pro_name)
    h = secret_key.objects.order_by("-id").filter(projects_name = pro.pro_name)
    return render_to_response('webkvm/show_key.html',locals())

@login_required
def show_key2(request):
    '''供admin用户查看密钥对'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    pro_projects = projects.objects.order_by('id').all()
    h = secret_key.objects.all().order_by("-id")
    return render_to_response('webkvm/show_key.html',locals())

@login_required
def create_key(request,id):
    '''创建密钥对'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if 'create_key' in request.GET and request.GET["create_key"]:
        key_name = request.GET['create_key']
        user = User.objects.get(username = username)
        user_id = user.id
        items = pro_user_relation.objects.filter(user_id = user_id)
        id_list = []
        for i in items:
            id_list.append(i.project_id)
        pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
        pro = projects.objects.get(id = id)
        try:
            secret_key.objects.get(secretkey_name = key_name)
        except Exception,e:
            from tasks import createkey
            createkey.delay(key_name)
            secret_key(secretkey_name = key_name,
                    create_person = username,
                    create_time = datetime.datetime.now(),
                    projects_name = pro.pro_name
                    ).save()
            html = "http://10.10.112.10/keypairs/download/%s" % key_name
            return render_to_response('webkvm/download_key.html',locals())
        return render_to_response('webkvm/error_key.html',locals())
    else:
        return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def create_key2(request):
    '''供admin用户创建密钥对'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if 'create_key' in request.GET and request.GET["create_key"]:
            key_name = request.GET['create_key']
            projects_key = request.GET['projects_key']
            try:
                secret_key.objects.get(secretkey_name = key_name)
            except Exception,e:
                from tasks import createkey
                createkey.delay(key_name)
                secret_key(secretkey_name = key_name,
                        create_person = username,
                        create_time = datetime.datetime.now(),
                        projects_name = projects_key
                        ).save()
                html = "http://10.10.112.10/keypairs/download/%s" % key_name
                return render_to_response('webkvm/download_key.html',locals())
            return render_to_response('webkvm/error_key.html',locals())
    else:
        return HttpResponseRedirect('/webkvm/manager_kvm/')

@login_required
def delete_key(request,id):
    '''删除密钥对'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = secret_key.objects.get(id = id)
    key_name = h.secretkey_name
    projects_name = h.projects_name
    pro = projects.objects.get(pro_name = projects_name)
    secret_key.objects.filter(secretkey_name = key_name).delete()
    from tasks import delkey
    delkey.delay(key_name)
    if username == 'admin':
        return HttpResponseRedirect('/webkvm/show_key/')
    return HttpResponseRedirect('/webkvm/show_key/%s/' % pro.id)

@login_required
def change_projects(request,id):
    '''切换项目'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if username != 'admin':
        user = User.objects.get(username = username)
        user_id = user.id
        items = pro_user_relation.objects.filter(user_id = user_id)
        id_list = []
        for i in items:
            id_list.append(i.project_id)
        pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
        pro = projects.objects.get(id = id)
        results = kvm_list.objects.filter(projects_name = pro.pro_name)
        return render_to_response("webkvm/change_projects.html",locals())
    else:
        pro_projects = projects.objects.all()
        pro = projects.objects.get(id = id)
        results = kvm_list.objects.filter(projects_name = pro.pro_name)
        return render_to_response("webkvm/change_projects.html",locals())

@login_required
def show_snap(request):
    '''admin用户在页面上查看快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    List = kvm_list.objects.order_by('-id')
    paginator = Paginator(List, 15)
    pro_projects = projects.objects.order_by('id').all()
    pro = pro_projects[0]
    keys = secret_key.objects.all()
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        List = paginator.page(page)
    except (EmptyPage, InvalidPage):
        List = paginator.page(paginator.num_pages)
    return render_to_response('webkvm/show_snap.html',
                                {'List':List,
                                'paginator':paginator,
                                'pro_projects':pro_projects,
                                'username':username,
                                'keys':keys,
                                'pro':pro
                                }
                                )

@login_required
def show_snap2(request, id):
    '''供普通用户查看快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    keys = secret_key.objects.all()
    user = User.objects.get(username = username)
    user_id = user.id
    items = pro_user_relation.objects.filter(user_id = user_id)
    id_list = []
    for i in items:
        id_list.append(i.project_id)
    pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
    pro = projects.objects.get(id = id)
    pro_name = []
    for i in pro_projects:
        pro_name.append(i.pro_name)
    List = kvm_list.objects.filter(projects_name = pro.pro_name)
    paginator = Paginator(List, 15)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        List = paginator.page(page)
    except (EmptyPage, InvalidPage):
        List = paginator.page(paginator.num_pages)
    return render_to_response('webkvm/show_snap.html',
                                {'List':List,
                                'paginator':paginator,
                                'pro_projects':pro_projects,
                                'username':username,
                                'keys':keys,
                                'pro':pro
                                }
                                )

@login_required
def zcloud_data(request):
    '''zcloud数据库备份信息'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = zcloud_size.objects.all()
    l = len(h) - 10
    return render_to_response('webkvm/zcloud.html',locals())

@login_required
def mirror_data(request):
    '''虚拟机镜像占用大小信息'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = mirror_size.objects.values_list()
    u = []
    v = []
    [u.append(i[1]) or v.append(i[3]) for i in h]
    name = list(set(u))
    create_time = list(set(v))
    create_time.sort()
    d = {}
    for i in name:
        d[i] = mirror_size.objects.filter(name = i)
    return render_to_response('webkvm/ceph_mirror.html',locals())