from django.db import models

class clouddisk(models.Model):
    image_name = models.CharField(max_length=20)
    size = models.CharField(max_length=50)
    mount_location = models.CharField(max_length=50,blank=True)
    ip = models.IPAddressField(max_length=50)
    dev_name = models.CharField(max_length=10)
    projects_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.image_name

class snap_clouddisk(models.Model):
    snap_id = models.CharField(max_length=20)
    image_name = models.CharField(max_length=20)
    snap_name= models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)
    snap_size = models.CharField(max_length=50)
    def __unicode__(self):
        return self.snap_name

class rollback_clouddisk(models.Model):
    snap_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)
    create_num = models.IntegerField(max_length=11,default=0)
    def __unicode__(self):
        return self.snap_name