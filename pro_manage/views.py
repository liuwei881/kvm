#coding=utf-8
from django.shortcuts import render,render_to_response
from pro_manage.models import projects,pro_user_relation
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from users.views import JsonHttpResponseReturn,userList
from django.utils.encoding import smart_str
from django.db import transaction
import time,json

def index(request):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    list = projects.objects.all()
    paginator = Paginator(list, 20)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
    return render_to_response('pro_manage/index.html',{'list':list,'paginator':paginator,'range10':xrange(1,201),'range20':xrange(3,201),'userList':userList(),'username':username})

# 新增
def add(request):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        post = request.POST
        data = {}
        data['pro_name']    = post.get('pro_name')
        data['pro_desc']    = post.get('pro_desc')
        data['c_cpu']       = int(smart_str(post.get('c_cpu')))
        #data['c_disk']      = int(smart_str(post.get('c_disk')))
        #data['c_space']     = int(smart_str(post.get('c_space')))
        data['c_memory']    = int(smart_str(post.get('c_memory')))
        data['admin_id']    = int(smart_str(post.get('admin_id')))
        data['create_id']   = request.user.id
        data['create_time'] = data['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        data['c_config'] = 0
        try:
            result = projects.objects.create(**data)
            print result
            print 'rs',type(result)
        except Exception,e:
           return JsonHttpResponseReturn({'status':500,'msg':e})
        if(result):
            return JsonHttpResponseReturn({'status':200,'msg':'新建成功'})
        else:
            return JsonHttpResponseReturn({'status':400,'msg':'新建项目失败'})


# 编辑
def edit(request):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        upData = {}
        try:
            userObj = projects.objects.filter(id=request.POST.get('pro_id'))
            upData['pro_desc']    = request.POST.get('pro_desc')
            upData['c_cpu']       = int(smart_str(request.POST.get('c_cpu')))
            #upData['c_disk']      = int(smart_str(request.POST.get('c_disk')))
            #upData['c_space']     = int(smart_str(request.POST.get('c_space')))
            upData['admin_id']    = int(smart_str(request.POST.get('admin_id')))
            upData['c_memory']    = int(smart_str(request.POST.get('c_memory')))
            result = userObj.update(**upData)
        except:
            return JsonHttpResponseReturn({'status':500,'msg':'请输入完整的用户信息'})
        if(result):
            return JsonHttpResponseReturn({'status':200,'msg':'修改成功'})
        else:
            return JsonHttpResponseReturn({'status':400,'msg':'修改用户失败'})

# 编辑项目成员信息
@transaction.atomic
def editProMembers(request,id):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST' and id:
        try:
            post = request.POST
            addUser = []
            for k in post:
                if post[k] == 'on':
                    if 'member' in k:
                        addUser.append(smart_str(k[10:]))
        except:
            return JsonHttpResponseReturn({'status':500,'msg':'数据处理失败'})
        try:
            pro_relative = pro_user_relation.objects.filter(project_id=id)
            pro_relative.delete()
            for uid in addUser:
                addData = {}
                addData['is_active'] = 1
                addData['user_id'] = uid
                addData['project_id'] = id
                pro_user_relation.objects.create(**addData)
            return JsonHttpResponseReturn({'status':200,'msg':'修改成功'})
        except Exception,e:
            return JsonHttpResponseReturn({'status':400,'msg':e})

def getProInfo(request,id):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    proInfo = projects.objects.get(id=id)
    print proInfo
    data = {}
    for key in proInfo.__dict__:
        data[key] = smart_str(proInfo.__dict__[key])
    del data['create_time'],data['update_time']
    print data
    if proInfo:
        return JsonHttpResponseReturn({'status':200,'msg':'ok','data':data})
    else:
        return JsonHttpResponseReturn({'status':400,'msg':'没有相关项目信息'})


# 获取项目的成员信息
def getProMembersInfo(request,id):
    username = request.session.get('username')
    if username == None:
        return HttpResponseRedirect('/login/')
    data = {}
    try:
        proMembersInfo = pro_user_relation.objects.values('user_id','id').filter(project_id=id)
        data['pro_name'] = projects.objects.values('pro_name').get(id=id)['pro_name']
    except:
        return JsonHttpResponseReturn({'status':500,'msg':'查询信息失败'})
    data['pro_id'] = id
    ulist = userList()
    html  = ''
    if proMembersInfo:
        data['list'] = list(proMembersInfo)
        alreadyUser = [m['user_id'] for m in proMembersInfo]
        for u in ulist:
            sel = 'checked' if u['id'] in alreadyUser else ''
            html = html + '<div class="checkbox"><label><input type="checkbox" name="member_id_%s" %s />%s</label></div>' % (smart_str(u['id']),sel,smart_str(u['username']))
    else:
        for u in ulist:
            html = html + '<div class="checkbox"><label><input type="checkbox" name="member_id_%s"/>%s</label></div>' % (smart_str(u['id']),smart_str(u['username']))
        data['list'] = []
    data['ht']=  html
    return JsonHttpResponseReturn({'status':200,'msg':'ok','data':data})

# 监控指定项目下各个虚拟机的 内存 cpu 等的使用情况
def getProUsedStatus(pro_id):
    pass