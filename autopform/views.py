#coding=utf-8
from django.shortcuts import render_to_response,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from pro_manage.models import projects,pro_user_relation
from django.contrib.auth.models import User
import json

def index(request):
	'''验证用户是否通过认证 '''
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	'''获取登录用户名'''
	username=request.session.get('username')
	pro_projects = projects.objects.order_by('id').all()
	pro = pro_projects[0]
	if username != 'admin':
		user = User.objects.get(username = username)
		user_id = user.id
		items = pro_user_relation.objects.filter(user_id = user_id)
		id_list = []
		for i in items:
			id_list.append(i.project_id)
		pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
		pro = pro_projects[0]
		return render_to_response('index2.html',{'username':username,'pro_projects':pro_projects,'pro':pro})
	return render_to_response('index.html',{'username':username,'pro_projects':pro_projects,'pro':pro})

def index2(request,id):
	'''划分项目'''
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	'''获取登录用户名'''
	username=request.session.get('username')
	user = User.objects.get(username = username)
	user_id = user.id
	items = pro_user_relation.objects.filter(user_id = user_id)
	id_list = []
	for i in items:
		id_list.append(i.project_id)
	pro_projects = projects.objects.order_by('id').filter(pk__in = id_list)
	pro = projects.objects.get(id = id)
	return render_to_response('index2.html',{'username':username,'pro_projects':pro_projects,'pro':pro})

def login(request):
	if request.method == "POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		if username is not None and password is not None:
			user=auth.authenticate(username=username,password=password)
			if user is not None and user.is_active:
				auth.login(request,user)
				#设置用户的session
				request.session['username']=username
				request.session.set_expiry(1800)
				return HttpResponseRedirect('/')
			else:
				return render_to_response('autopform/login_error.html')
		else:
			return HttpResponseRedirect('/login/')
	'''判断是否已经登录'''
	if request.user.is_authenticated() and request.session['username'] is not None:
		return HttpResponseRedirect('/')
	else:
		return render_to_response('autopform/login.html')

def logout(request):
	'''用户登出'''
	auth.logout(request)
	request.session['username'] = None
	return HttpResponseRedirect('/login/')

def changepasswd(request):
	'''更改用户密码'''
	username = request.session.get('username')
	try:
		if 'source_password' in request.GET and request.GET["source_password"]:
			source_password = request.GET['source_password']
			password = request.GET['new_password']
			confirm_password = request.GET['confirm_password']
			if password != confirm_password:
				return HttpResponse(json.dumps({'status':200,'msg':'两次密码一样,请重新输入'}), content_type="application/json")
			else:
				user = User.objects.get(username = username)
				if user.check_password(source_password):
					user.set_password(password)
					user.save()
					return HttpResponse(json.dumps({'status':200,'msg':'修改密码成功'}), content_type="application/json")
				else:
					return HttpResponse(json.dumps({'status':200,'msg':'原密码不正确，请重新输入'}), content_type="application/json")
	except Exception,e:
		return HttpResponse(json.dumps({'status':200,'msg':"修改失败"}), content_type="application/json")