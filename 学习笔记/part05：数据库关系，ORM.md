# Django学习p5：数据库关系，ORM

## 一对一，一对多，多对多

Django的各个表的关系主要通过 `django.db.models` 中的方法实现：

- 一对一：`models.OneToOneField([要建立关系的另一表类], on_delete=)`
- 一对多：`models.ForeignKey([被关联主键的表类], on_delete=)`
- 多对多：`models.ManyToManyField([要建立关系的另一个表], through=)`
  - through指定了一个中间关系的表项，不是必填字段。例如`药品`和`订单`的多对多关系可以通过`药品订单`实现。
  - 同时多对多也可以借助 `ForeignKey()` 来建立，通过设立一个中间表来间接实现多对多关系
其中 `on_delte` 字段提供了三种模式：

- `CASCADE`：删除主键记录和相应的外键表记录
- `PROTECT`：所有相关联的记录都禁止删除（例如有5个订单的外键与张三的主键关联，那得先删除这5个订单才能删除张三）
- `SET_NULL`：删除主键记录时，外键记录相关字段设为null（前提是允许设为null）

下面是一个简单的示例：
```python
from django.db import models

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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)    # 与顾客建立一对多关系

class OrderMedicine(models.Model):
    """协助 Medicine 和 Order 建立多对多关系"""
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    # 药品数量
    amount = models.PositiveIntegerField()
```
通过对这些表类的处理基本上类似[part03](./part03：增删改查，登录.md)

## ORM

### 创建数据库与查询

对象关系映射ORM是用于将对象与关系型数据库中的数据表之间进行映射的技术。

以下创建 国家表`Country` 和 学生表`Student` 作为示例：
```python
class Country(models.Model):
    name = models.CharField(max_length=100)
class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.PositiveSmallIntegerField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='students')
```

可以通过 ```python manage.py shell``` 命令，来直接输入并运行一些脚本，例如说现在需要添加Country表和Student表中的数据：
```python
from common.models import *
c1 = Country.objects.create(name='中国')
Student.objects.create(name='白月', grade=1, country=c1)
```
<br>

而在Django ORM中，可以通过如下方式来实现通过外键表的其它信息来获得当前表所需查找的外键目标。  
例如学生表的国家信息是关联了自国家表id的外键，但我们又想通过国家名来更高效地过滤学生信息，则可以在 `filter()` 中，
采取双下划线的方式调用外键对应表的数据:  
```python
Student.objects.filter(grade=1, country__name='中国').values('name','country__name')
```  
``❗❗注意是两条下划线``  

同时可以使用 django.db.models.F() 来实现对返回信息的重命名：
```python
Student.objects.annotate(
    countryName=F('country__name'), 
    studentName=F('name')
).filter(grade=1, country__name='中国').values('studentName', 'countryName')
```
可以通过外键表的部分信息查找与之关联表的信息，例如根据已有Country对象访问属于此国家的全部学生：
```python
Country.objects.get(name='中国').student_set.all().values()   # 将学生表小写并补上 _set 来获取所有反向外键的关联对象
```
若需要去重，可以使用 distinct()： 
```python
Country.objects.filter(student__grade=1).values().distinct()
```
如果对应的 `ForeignKey()` 有定义反向访问字段 related_name= 则`必须`使用指定的反向访问名字（例如 =students ）:
```python
Country.objects.get(name='中国').students.all().values()
```

### 对数据库进行功能操作

大体上的增删改查操作与 [part03](./part03：增删改查，登录.md) 无异。  
涉及到对两张表的关系查询可参照上述提到的方式。  
涉及对两张表更改的操作，可以引入原子操作 `django.db.transaction.atomic()`，具体使用方式可以参考下列代码。  
```python
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
import json
# 导入Order对象的定义
from common.models import Order, OrderMedicine

def dispatcher(request):

    # 根据session判断用户是否登陆了管理员账户
    if 'usertype' not in request.session:
        return  JsonResponse({'ret':302, 'msg':'未登录', 'redirect':'/mngr/sign.html'}, status=302)
    if request.session['usertype'] != 'mngr':
        return JsonResponse({'ret':302, 'msg':'用户不是mngr类型', 'redirect':'/mngr/sign.html'}, status=302)

    # 将请求参数统一放入request的params属性中，方便后续处理

    # GET请求参数在request对象的GET属性中
    if request.method == 'GET': request.params = request.GET
    # POST/PUT/DELETE请求参数从request对象的body属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']: request.params = json.loads(request.body)

    # 根据不同action分派给不同函数进行处理
    action = request.params['action']
    if action == 'list_order': return listOrder(request)
    if action == 'add_order': return addOrder(request)
    """暂定订单不支持修改和删除"""
    return JsonResponse({'ret':1, 'msg':'不支持该类型http请求'})


def addOrder(request):
    info = request.params['data']
    # 根据文档提供的接口，添加订单的操作会涉及两张表。因此将对两张表的操作整合在一个事务中进行（原子性）
    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'], customer_id=info['customerid'])
        batch = [
            OrderMedicine(order_id=new_order.id,medicine_id=mid,amount=1) for mid in info['medicineids']
        ]   # 根据接口，一个订单可能会涉及多种药品，故采取批量操作
        OrderMedicine.objects.bulk_create(batch)    # bulk_create()是一个批量创建记录的方
    return JsonResponse({'ret':0, 'id':new_order.id})


def listOrder(request):

    # 获取数据
    qs = Order.objects.annotate(
        customer_name=F('customer__name'),
        medicines_name=F('medicines__name')
    ).values('id','name', 'create_date', 'customer_name', 'medicines_name')
    retList = list(qs)  # 将QuerySet对象转化为list

    # 合并ID相同、但药品不同的订单记录
    newList = []
    id2order = {}
    for one in retList:
        orderID = one['id']
        if orderID not in id2order:
            newList.append(one)
            id2order[orderID] = one
        else:
            id2order[orderID]['medicines_name'] += '|' + one['medicines_name']

    return JsonResponse({'ret':0, 'retlist':retList})
```

