#coding=utf-8

from django import forms

class HostAddForm(forms.Form):
	ip = forms.IPAddressField(label="主机ip")
	username = forms.CharField(label="用户名")
	port = forms.CharField(max_length=5,label="端口")
	runcmd = forms.CharField(max_length=5,label="执行命令")
