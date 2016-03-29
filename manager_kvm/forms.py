#coding=utf-8
import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import kvm_tag 


class kvm_form(forms.Form):
	kvm_name = forms.CharField(max_length=20)
	vir_name = forms.CharField(max_length=20)
	vir_os = forms.CharField(max_length=100)
	vir_memory = forms.CharField(max_length=100)
	vir_disk = forms.CharField(max_length=100)
	vir_cpu = forms.CharField(max_length=100)
	
	def clean_vir_name(self):
		vir_name = self.cleaned_data['vir_name']
		have_symbol = re.match('[^a-zA-Z0-9._-]+', vir_name)
		if have_symbol:
			raise forms.ValidationError(_('请输入正确的虚拟机名字'))
		elif len(vir_name) > 20:
			raise forms.ValidationError(_('虚拟机的长度不能大于20个字符串'))
		try:
			kvm_tag.objects.get(vir_name=vir_name)
		except kvm_tag.DoesNotExist:
			return vir_name
		raise forms.ValidationError(_('已经选好虚拟机'))
