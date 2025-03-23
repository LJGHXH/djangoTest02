import datetime

from django.db import models
from django.contrib import admin

# Create your models here.


class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=100)
    # 联系电话
    phoneNumber = models.CharField(max_length=11)
    # 地址
    address = models.CharField(max_length=200)
    # QQ号
    qq = models.CharField(max_length=30, null=True, blank=True)
    # # 用户状态
    # state = models.BooleanField(default=True)


admin.site.register(Customer)


class Medicine(models.Model):
    # 药品名
    name = models.CharField(max_length=100)
    # 药品编号
    sn = models.CharField(max_length=100)
    # 描述
    desc = models.CharField(max_length=200)


class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200, null=True, blank=True)
    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)    # 告诉Django：customer字段是指向Customer表主键的一个外键
    """
    on_delete字段有三种模式，对应不同操作：
        CASCADE：删除主键记录和相应的外键表记录
        PROTECT：所有相关联的记录都禁止删除（例如有三个订单的外键与张三的主键关联，那得先删除这三个订单才能删除张三）
        SET_NULL：删除主键记录时，外键记录相关字段设为null（前提是允许设为null）
    """
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')


"""
Django的各个数据库关系的实现：
    一对一：models.OneToOneField([要建立关系的另一表类], on_delete=)
    一对多：models.ForeignKey([被关联主键的表类], on_delete=)
    多对多：models.ManyToManyField([要建立关系的另一个表], through=)  # through指定了一个中间关系的表项，不是必填字段
"""


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    # 药品数量
    amount = models.PositiveIntegerField()


"""为了方便学习ORM，以下添加两张练习用的表"""
class Country(models.Model):
    name = models.CharField(max_length=100)
class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.PositiveSmallIntegerField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='students')
