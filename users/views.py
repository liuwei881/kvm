#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
import json
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.hashers import make_password
from django.db import transaction

# 用户列表
def index(request):
    username = request.session.get('username')
    if username == 'admin':
        list = User.objects.order_by('-id')
    else:
        list = User.objects.filter(username = username)
    paginator = Paginator(list, 20)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
    return render_to_response('users/index.html',{'list':list,'paginator':paginator,'username':username})

# 新增用户
def add(request):
    if request.method == 'POST':
        try:
            result = User.objects.create_user(request.POST.get('username'),request.POST.get('email'),{'password':request.POST.get('password'),'is_active':int(request.POST.get('is_active'))})
            print result
        except:
            return JsonHttpResponseReturn({'status':500,'msg':'请输入完整的用户信息'})
        if(result):
            return JsonHttpResponseReturn({'status':200,'msg':'新建成功'})
        else:
            return JsonHttpResponseReturn({'status':400,'msg':'新建用户失败'})

# 编辑用户
def edit(request):
    if request.method == 'POST':
        upData = {}
        #try:
        userObj = User.objects.filter(id=request.POST.get('id'))
        upData['email'] = request.POST.get('email')
        upData['is_active'] = int(request.POST.get('is_active'))
        if len(request.POST.get('password'))>2:
            upData['password'] = make_password(request.POST.get('password'))
        result = userObj.update(**upData)
        print result
        # except:
        #     return JsonHttpResponseReturn({'status':500,'msg':'请输入完整的用户信息'})
        if(result):
            return JsonHttpResponseReturn({'status':200,'msg':'修改成功'})
        else:
            return JsonHttpResponseReturn({'status':400,'msg':'修改用户失败'})

# 修改用户状态 _active
def changeStatus(request):
    userInfo = User.objects.filter(id=request.GET.get('id'))
    status = int(request.GET.get('status'))
    result =  userInfo.update(is_active = status)
    if result:
        return JsonHttpResponseReturn({'status':200,'msg':'修改成功'})
    else:
        return JsonHttpResponseReturn({'status':400,'msg':'修改失败，请重试'})

# 获取用户相关的项目信息
def getUserProInfo(request,id):
    from pro_manage.models import *
    from django.utils.encoding import smart_str
    proLIst = projects.objects.values('id','pro_name').all()    # 全部项目
    urList = pro_user_relation.objects.values('project_id').filter(user_id=id)          # 用户项目
    pList = [u['project_id'] for u in urList]
    data = {}
    data['proList'] = list(proLIst)
    data['user_id'] = id
    data['username'] = User.objects.values('username').get(id=id)['username']
    html = ''
    for p in proLIst:
        ck = ('checked ' if p['id'] in pList else  '')
        html = html + '<div class="checkbox"><label><input type="checkbox" name="pro_id_%s" %s value="%s" />%s</label></div>' % (smart_str(p['id']),ck, smart_str(p['id']), smart_str(p['pro_name']))
    data['html'] = html
    return JsonHttpResponseReturn({'status':200,'msg':'修改失败，请重试','data':data})

# 修改用户所在项目组
@transaction.atomic
def editUserProInfo(request,id):
    if request.method == 'POST' and id:
        from pro_manage.models import pro_user_relation
        from django.utils.encoding import smart_str
        #try:
        allInsData = []
        for key in request.POST:
            if 'pro_id' in key:
                insData = {}
                insData['project_id']   = int(smart_str(key[7:]))
                insData['user_id']      = id
                insData['is_active']    = 1
                insData['is_admin']     = 0
                allInsData.append(pro_user_relation(**insData))
        oldData = pro_user_relation.objects.filter(user_id=id)
        oldData.delete()
        pro_user_relation.objects.bulk_create(allInsData)
        return JsonHttpResponseReturn({'status':200,'msg':'修改成功'})
        # except:
        #     return JsonHttpResponseReturn({'status':400,'msg':'修改失败'})
    else:
        return JsonHttpResponseReturn({'status':500,'msg':'参数缺失，请重试'})

# 获取单个用户信息
def getUserInfo(request,id):
    userInfo = User.objects.get(id=id)
    data = {}
    for key in userInfo.__dict__:
        data[key] = userInfo.__dict__[key]
    del data['password'],data['_state'],data['date_joined'],data['last_login']
    if userInfo:
        return JsonHttpResponseReturn({'status':200,'msg':'修改成功','data':data})
    else:
        return JsonHttpResponseReturn({'status':400,'msg':'没有相关用户信息'})

def JsonHttpResponseReturn(dict):
    return HttpResponse(json.dumps(dict), content_type="application/json")

def userList(is_active=1):
    if is_active:
        list = User.objects.values('id','username').filter(is_active=1)
    else:
        list = User.objects.values('id','username').filter()
    return list