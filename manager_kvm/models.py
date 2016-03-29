from django.db import models
from webkvm.models import kvm_list

class snapshot_show(models.Model):
    hostname = models.ForeignKey(kvm_list)
    s_hostname = models.CharField(max_length=50)
    snapshot_name= models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)
    snapshot_num = models.CharField(max_length=50)
    auto_create = models.CharField(max_length=50)
    def __unicode__(self):
        return self.snapshot_name