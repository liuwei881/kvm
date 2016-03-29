from django.contrib import admin
from webkvm.models import kvmtag,kvm_list

class kvmAdmin(admin.ModelAdmin):
	list_display = [
                'hostname',
                'ip',
                'ip1',
                'ip2',
                'location',
                'salt_status',
                ]
	search_fields = ('hostname',)

admin.site.register(kvmtag,kvmAdmin)

class kvmvir(admin.ModelAdmin):
    list_display = [
                'hostname',
                'ip',
                'vir_disk',
                'location',
                'kvm_location',
                'create_time',
                'host_status',
                'main_host',
                ]
    search_fields = ('hostname',)

admin.site.register(kvm_list,kvmvir)
