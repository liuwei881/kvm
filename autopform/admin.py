from django.contrib import admin

from autopform.models import serviceip

class Ip(admin.ModelAdmin):
    list_display = ('ip','port')

admin.site.register(serviceip, Ip)
