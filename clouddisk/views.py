#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import json,random
import salt.client
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import clouddisk,snap_clouddisk,rollback_clouddisk
from webkvm.models import kvm_list
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from pro_manage.models import projects,pro_user_relation

@login_required
def clouddisk_index(request,id):
    '''准备创建ceph镜像'''
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
    h = clouddisk.objects.order_by('-id').filter(projects_name = pro.pro_name)
    paginator = Paginator(h, 10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        h = paginator.page(page)
    except (EmptyPage, InvalidPage):
        h = paginator.page(paginator.num_pages)
    vm_ip = kvm_list.objects.all()
    return render_to_response("clouddisk/add_image.html",{'h':h,'vm_ip':vm_ip,'username':username,'pro_projects':pro_projects,'pro':pro,'paginator':paginator})

@login_required
def clouddisk_index2(request):
    '''admin用户访问,准备创建ceph镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = clouddisk.objects.order_by('-id')
    paginator = Paginator(h, 10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        h = paginator.page(page)
    except (EmptyPage, InvalidPage):
        h = paginator.page(paginator.num_pages)
    vm_ip = kvm_list.objects.all()
    pro_projects = projects.objects.order_by('id').all()
    return render_to_response("clouddisk/add_image.html",{'h':h,'vm_ip':vm_ip,'username':username,'pro_projects':pro_projects,'paginator':paginator})

@login_required
def addclouddisk(request):
    '''创建ceph镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = clouddisk.objects.all()
    vm_ip = kvm_list.objects.all()
    try:
        if 'image_name' in request.GET and request.GET["image_name"]:
            image_name = request.GET['image_name']
            size = request.GET['size']
            size = int(size[0:-1]) * 1024
            try:
                clouddisk.objects.get(image_name = image_name)
                return HttpResponse(json.dumps({'status':200,'msg':'rdb镜像不能重名'}), content_type="application/json")
            except Exception,e:
                local = salt.client.LocalClient()
                hostname_list = ['ceph01-10-10-111-1.iprun.com','ceph02-10-10-111-2.iprun.com','ceph04-10-10-111-4.iprun.com']
                hostname = random.choice(hostname_list)
                local.cmd("%s" % hostname,"cmd.run",["rbd create %s --size %s --pool kvms" % (image_name,size)])   #客户端要自己定义
                if username == 'admin':
                    clouddisk(image_name=image_name,size=size,mount_location='',ip='',dev_name='',projects_name='').save()
                    return HttpResponse(json.dumps({'status':200,'msg':'创建rdb镜像完成'}), content_type="application/json")
                else:
                    user = User.objects.get(username = username)
                    user_id = user.id
                    items = pro_user_relation.objects.filter(user_id = user_id)
                    id_list = []
                    for i in items:
                        id_list.append(i.project_id)
                    pro_projects = projects.objects.filter(pk__in = id_list)
                    pro_name = []
                    for i in pro_projects:
                        pro_name.append(i.pro_name)
                    projects_name = random.choice(pro_name)
                    clouddisk(image_name=image_name,size=size,mount_location='',ip='',dev_name='',projects_name=projects_name).save()
                    return HttpResponse(json.dumps({'status':200,'msg':'创建rdb镜像完成'}), content_type="application/json")
        else:
            pass
    except Exception,e:
        return render_to_response("clouddisk/add_image.html",{'h':h,'vm_ip':vm_ip,'username':username})

@login_required
def search_clouddisk(request):
    '''查询云硬盘镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    query = request.GET.get('q','')
    if query:
        qset= (
            Q(image_name__icontains = query)|
            Q(mount_location__icontains = query)|
            Q(ip__icontains = query)
        )
        results = clouddisk.objects.filter(qset)
    else:
        results = []
    return render_to_response("clouddisk/search_clouddisk.html",{"results":results,'username':username})

@login_required
def mountclouddisk(request,id):
    '''显示ceph镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = clouddisk.objects.get(id = id)
    vm_ip = kvm_list.objects.all()
    return render_to_response("clouddisk/mount_image.html",{'h':h,'vm_ip':vm_ip,'username':username})

@login_required
def delimage(request,id):
    '''删除ceph镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        h = clouddisk.objects.all()
        i = clouddisk.objects.get(id = id)
        vm_ip = kvm_list.objects.all()
        image_name = i.image_name
        from tasks import del_image
        del_image.delay(image_name)
        clouddisk.objects.get(image_name = image_name).delete()
        return render_to_response("clouddisk/add_image.html",{'h':h,'vm_ip':vm_ip,'username':username})
    except Exception,e:
        return HttpResponseRedirect('/clouddisk/')

@login_required
def mountdisk(request,id):
    '''挂载ceph镜像'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = clouddisk.objects.get(id = id)
    image_name = h.image_name
    try:
        if "cloud_name" in request.GET and request.GET["cloud_name"]:
            cloud_name = request.GET["cloud_name"]
            vm_hostname = kvm_list.objects.get(cloud_name = cloud_name).hostname
            main_host = kvm_list.objects.get(cloud_name = cloud_name).main_host
            ip = kvm_list.objects.get(cloud_name = cloud_name).ip
            projects_name = kvm_list.objects.get(cloud_name = cloud_name).projects_name
            dict_disk = {1:'vdb',2:'vdc',3:'vdd',4:'vde',5:'vdf',6:'vdg',7:'vdh',8:'vdi'}
            if len(clouddisk.objects.filter(mount_location = h.mount_location)) == 1 and h.mount_location == '':
                dev_name = dict_disk[1]
            else:
                dev_name = dict_disk[len(clouddisk.objects.filter(mount_location = h.mount_location)) + 1]
            from tasks import mount_disk
            host = ('10.10.111.1','10.10.111.2','10.10.111.4')
            host_name = random.choice(host)
            mount_disk.delay(main_host,image_name,vm_hostname,ip,dev_name,host_name)
            clouddisk(image_name = image_name,size = h.size,mount_location = cloud_name,ip = ip,dev_name = dev_name,projects_name = projects_name).save()
            clouddisk.objects.get(image_name = image_name, ip ='', mount_location='').delete()
            return HttpResponseRedirect('/clouddisk/')
        else:
            print "ok"
    except Exception,e:
        return HttpResponseRedirect('/clouddisk/')

@login_required
def umountdisk(request,id):
    '''云硬盘卸载'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        h = clouddisk.objects.get(id = id)
        image_name = h.image_name
        cloud_name = h.mount_location
        dev_name = h.dev_name
        vm_hostname = kvm_list.objects.get(cloud_name = cloud_name).hostname
        main_host = kvm_list.objects.get(cloud_name = cloud_name).main_host
        ip = kvm_list.objects.get(cloud_name = cloud_name).ip
        projects_name = kvm_list.objects.get(cloud_name = cloud_name).projects_name
        from tasks import umount_disk
        umount_disk.delay(main_host,vm_hostname,image_name,ip,dev_name)
        clouddisk.objects.get(mount_location = cloud_name,image_name = image_name).delete()
        if list(clouddisk.objects.filter(image_name = image_name)) == []:
            clouddisk(image_name = image_name,size = h.size,mount_location = '',ip='',dev_name='',projects_name=projects_name).save()
        else:
            pass
        return HttpResponseRedirect('/clouddisk/')
    except Exception,e:
        return HttpResponseRedirect('/clouddisk/')

@login_required
def showcloudsnap(request, id):
    '''准备创建ceph快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = clouddisk.objects.get(id = id)
    return render_to_response("clouddisk/edit_snap.html",{'h':h,'username':username})

@login_required
def snapshotclouddisk(request, id):
    '''创建ceph快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        if 'snap_name' in request.GET and request.GET["snap_name"]:
            snap_name = request.GET["snap_name"]
            h = clouddisk.objects.get(id = id)
            image_name = h.image_name
            from tasks import snap_disk
            snap_disk.delay(image_name,snap_name)
            return render_to_response("clouddisk/succeed_snap.html",{'h':h,'username':username})
        else:
            pass
    except Exception,e:
        h = clouddisk.objects.get(id = id)
        username = request.session.get('username')
        return render_to_response("clouddisk/error_snap.html",{'h':h,'e':e,'username':username})

@login_required
def showclouddisk(request, id):
    '''查看ceph快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        h = clouddisk.objects.get(id = id)
        image_name = h.image_name
        snap_size = h.size
        show_snap = snap_clouddisk.objects.all()
        local = salt.client.LocalClient()
        a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",["rbd snap ls -p kvms %s" % image_name]) #kvms01 为mon 6789端口主机
        snap_id = a.values()[0].split("\n")[-1].split(' ')[-4]
        snap_name = a.values()[0].split("\n")[-1].split(' ')[-3]
        snap_list = snap_clouddisk.objects.filter(snap_id = snap_id).values()
        if list(snap_list) == []:
            snap_clouddisk(image_name = image_name,
                           snap_name = snap_name,
                           snap_size = snap_size,
                           snap_id = int(snap_id)
                           ).save()
            return render_to_response("clouddisk/show_snap.html",{'h':h,'show_snap':show_snap,'username':username})
        else:
            return render_to_response("clouddisk/show_snap.html",{'h':h,'show_snap':show_snap,'username':username})
    except Exception,e:
        return render_to_response("clouddisk/nohave_snap.html",{'username':username})

@login_required
def delclouddisk(request,id,k):
    '''删除ceph快照'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    try:
        h = snap_clouddisk.objects.get(id = id,snap_id = k)
    except Exception,e:
        return render_to_response("clouddisk/del_error_snap.html",{'username':username})
    show_snap = snap_clouddisk.objects.all()
    image_name = h.image_name
    snap_name = h.snap_name
    try:
        from tasks import del_snap
        del_snap.delay(image_name,snap_name)
        snap_clouddisk.objects.filter(snap_name = snap_name).delete()
        return render_to_response("clouddisk/show_snap.html",{'h':h,'show_snap':show_snap,'username':username})
    except Exception,e:
        return render_to_response("clouddisk/del_snap.html",{'h':h,'e':e,'username':username})

@login_required
def rollbackclouddisk(request,id,k):
    '''从ceph快照恢复'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = snap_clouddisk.objects.get(id = id,snap_id = k)
    show_snap = snap_clouddisk.objects.all()
    image_name = h.image_name
    snap_name = h.snap_name
    from tasks import rollback_snap
    rollback_snap.delay(image_name,snap_name)
    create_num = len(rollback_clouddisk.objects.filter(snap_name = snap_name))
    create_num += 1
    rollback_clouddisk(snap_name = snap_name,create_num = create_num).save()
    return render_to_response("clouddisk/show_snap.html",{'h':h,'show_snap':show_snap,'username':username})

@login_required
def rollback_log(request,id,k):
    '''查看快照回滚日志'''
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    h = snap_clouddisk.objects.get(id = id,snap_id = k)
    h_id = clouddisk.objects.get(image_name = h.image_name)
    rollback = rollback_clouddisk.objects.all()
    return render_to_response("clouddisk/rollbacklog_snap.html",{'h':h,'rollback':rollback,'h_id':h_id,'username':username})