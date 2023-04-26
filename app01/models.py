from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()

    # 这个类相当于在mysql中写入语句：
    # create table app01_userinfo(
    #     id big int auto_increment primary key,
    #     name varchar(32),
    #     password varchar(32),
    #     age int
    # );

class Department(models.Model):
    title = models.CharField(max_length=32)

# 新建数据 insert into app01_department(title) values('销售部');
# Department.objects.create(title='销售部')