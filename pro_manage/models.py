#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# 项目表
class projects(models.Model):
    pro_name = models.CharField(max_length = 100)
    pro_desc = models.CharField(max_length = 254, blank = True)
    c_cpu = models.IntegerField(default = 1)       # cpu 数量
    v_cpu = models.IntegerField(default = 1)            # 已分配cpu数量
    c_memory = models.IntegerField(default = 1)         # 内存数量
    v_memory = models.IntegerField(default = 1)         # 已分配内存数量
    c_space = models.IntegerField(default=100)          # 空间配额 单位G
    c_disk = models.SmallIntegerField(default = 1)      # 硬盘数
    c_config = models.IntegerField(default = 1)           # 其他配置
    status = models.SmallIntegerField(default = 1)      # 已创建1 进行中2   完成3  删除4  。。。
    # admin_id  = models.IntegerField()                   # 负责人
    admin  = models.ForeignKey(User)                   # 负责人
    #create_id  = models.IntegerField()                  # 创建人
    create  = models.ForeignKey(User)                  # 创建人
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
       db_table = 'pro_projects'
       ordering =['-id']
    def __unicode__(self):
        return self.pro_name
    # def doSave(self,*agrs,**kwargs):
    #     self.c_cpu = int(smart_str(self.c_cpu))
    #     self.c_space = int(smart_str(self.c_space))
    #     self.c_disk = int(smart_str(self.c_disk))
    #     super(projects,self).save()

# 用户关系项目表   暂不考虑用户组
class pro_user_relation(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    # date_joined = models.DateTimeField(auto_now_add=True)
    # date_lefted = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1)
    # is_admin = models.BooleanField(default=0)

    class Meta:
       db_table = 'pro_user_relation'
    def __unicode__(self):
        return self.project_id

# 项目 虚拟机关系