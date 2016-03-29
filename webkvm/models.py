from django.db import models

class kvmtag(models.Model):
    hostname = models.CharField(max_length=20)
    ip = models.IPAddressField(max_length=50)
    ip1 = models.IPAddressField(max_length=50)
    ip2 = models.IPAddressField(max_length=50)
    location = models.CharField(max_length=50)
    osversion = models.CharField(max_length=20)
    memory = models.CharField(max_length=20)
    disk = models.CharField(max_length=20)
    model_name = models.CharField(max_length=50)
    cpu_core = models.CharField(max_length=20)
    sorts = models.CharField(max_length=20)
    salt_status = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.hostname

class kvm_list(models.Model):
    cloud_name = models.CharField(max_length=40)
    hostname = models.CharField(max_length=20)
    ip = models.IPAddressField(max_length=50)
    vir_disk = models.CharField(max_length=20)
    main_host = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)
    kvm_location = models.CharField(max_length=40)
    create_time = models.DateTimeField(auto_now_add=True)
    host_status = models.CharField(max_length=10,default='Unkown')
    projects_name = models.CharField(max_length=50)
    mirror_name = models.CharField(max_length=50)
    secret_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.cloud_name
    class Meta:
        ordering = ['-create_time']

class mirrorname(models.Model):
    mirror_name = models.CharField(max_length=50)
    level = models.IntegerField(max_length=2)
    parent = models.IntegerField(max_length=2)
    def __unicode__(self):
        return self.mirror_name
    class Meta:
        db_table = 'mirrorname'

class secret_key(models.Model):
    secretkey_name = models.CharField(max_length=20)
    create_person = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    projects_name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.secretkey_name
    class Meta:
        db_table = 'secretkey'

class zcloud_size(models.Model):
    size = models.CharField(max_length=20)
    create_time = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.size
    class Meta:
        db_table = 'zcloud_size'

class mirror_size(models.Model):
    name = models.CharField(max_length=30)
    size = models.CharField(max_length=20)
    create_time = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return u'%s %s %s'.format(self.name,self.size,self.create_time)
    class Meta:
        db_table = 'mirror_size'
