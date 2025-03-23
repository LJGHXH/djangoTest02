# Django学习p2：数据库创建，数据库管理员注册，访问数据库

## 创建一个新的数据库应用

先创建一个存放公共表项的common目录，所需指令为：
```commandline
python manage.py startapp common
```
随后需要在 `settings.py` 中的 `INSTALLED_APPS` 里添加 `'common.apps.CommonConfig'`，
来告诉Django `CommonConfig`是 `common/apps.py` 中定义的一个应用配置类。其它的配置参数可以参考：
https://docs.djangoproject.com/en/dev/ref/applications/#configurable-attributes 。

这样我们就可以在 `common/models.py` 中定义新表的类，例如这里创建一个 `Custmor` 类：
```python
from django.db import models

class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=100)
    # 联系电话
    phoneNumber = models.CharField(max_length=11)
    # 地址
    address = models.CharField(max_length=200)
```
然后在命令行中依次输入如下命令，来让Django更新脚本，以及更新数据库（`日后每次修改类都需要执行这两句命令`）：
```commandline
python manage.py makemigrations common
python manage.py migrate
```
若表类更新了新的表项，则最好需要设置其默认值（或允许其为空），例如：
```python
    qq = models.CharField(max_length=30, null=True, blank=True)
```
随后再执行上述两条指令更新数据库即可。同时也可以随时删除类中的变量来删除表项。

## 管理数据库

Django自带一个管理员页面，需要先注册一个管理员账户以登录该页面。输入如下命令，并设置好用户名、邮箱、密码:
```commandline
python manage.py createsuperuser
```

随后即可用该账号登录 `127.0.0.1/admin/`。可以将该页面改成当地语言，
在 `settings.py` 中的 `MIDDLEWARE` 添加 `'django.middleware.locale.LocaleMiddleware',` 即可。

同时为了将我们之前创建好的表类添加到数据库并可在管理员页面管理，可在 `common/models.py` 或 `common/admin.py` 中添加如下内容：
```python
from django.contrib import admin

admin.site.register(Customer)
```

## 访问数据库内容

可以在 `urls.py` 中自定义一个路由（以 `127.0.0.1/sales/customer/` 为例），并在 `views.py` 中编写对应功能。
例如我们要查找 `Customer类` 中的表项，可以参考如下：
```python
from common.models import Customer

def listCustomer(request):
    # type(qs) = <QuerySet>，其包含读取到的所有记录。每条记录都是一个dict对象（key是字段名，value是字段值）
    qs = Customer.objects.values()      # objects 来自 models.Model
    # 定义返回字符串
    retStr = ''
    for customer in qs:
        for name, value in customer.items():
            retStr += f'{name} : {value} | '
        retStr += '</br>'
    return HttpResponse(retStr)
```
若需要查找指定内容，例如根据电话号码查找，则可在 `listCustomer()` 中添加如下语句：
```python
    # 根据url中的phoneNumber查询
    pn = request.GET.get('phonenumber', None)   # 注意，url在浏览器刷新时会自动全转为小写，所以此处冒号内不要出现大写
    if pn:
        qs = qs.filter(phoneNumber=pn)
```
然后访问url `127.0.0.1/salers/customer/?phonenumber=[待查表项的电话]` 即可。

## 前后端分离

后端提供纯数据（例如JSON格式的API），前端通过API获取数据独立完成渲染。

让我们的数据在前端界面中规整一些，例如配合制表符，可将上述 `listCustomer()` 的代码修改为：
```python
    for customer in qs:
        retStr += '<tr>'
        for name, value in customer.items():
            retStr += f'<td> {value} </td>'
        retStr += '</br>'
    # 然后配合已写好的前端页面
    from django.template import loader
    customer_template = loader.get_template('customerTemplate.html')    # 以模板形式(Django的Template)获取html文件，适用于render()
    customer_template = customer_template.render()      # 将模板转换为字符串形式(Django的SafeString)
    # 返回我们所需要的内容
    return HttpResponse(customer_template%retStr)
    '''
    在 customerTemplate.html 中，会用 %s 来告诉后端上述字符串在前端中的位置
    '''
```

通常来说后端只需要提供数据，具体的修饰内容可由前端开发者决定，故可在 html 文件中按如下方式来排版后端数据：
```html
    {% for customer in customers %}
        <tr>

        {% for name, value in customer.items %}
            <td>{{ value }}</td>
        {% endfor %}

        </tr>
    {% endfor %}
```
可以看得出来基本和后端的python语言很类似。  
而后端也可以利用 `django.template.engines` 来引用模板引擎来传入渲染模板所需的参数：
```python
from django.template import engines

django_engine = engines['django']
with open("D:/CODE/Python/WebCoding/djangoTest02/htmlFiles/customerTemplateTutorial.html", "r", encoding="utf-8") as file:
    customer_template = file.read()
template = django_engine.from_string(customer_template)

def listCustomer2(request):
    qs = Customer.objects.values()
    rendered = template.render({'customers':qs})
    return HttpResponse(rendered)
```
对于模板的详细用法，可参考：https://docs.djangoproject.com/zh-hans/5.1/topics/templates/
