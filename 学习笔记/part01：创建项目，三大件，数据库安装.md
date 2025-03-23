# Django学习p1：创建项目，三大件，数据库安装
## 创建一个新的Django项目并运行

在命令行中输入: 
```commandline
django-admin startproject [你的项目名]
```
运行这个Django项目：
```commandline
python manage.py runserver [你期望的ip:端口号]
```
可以在 `/[项目名]/settings.py` 中修改 ALLOWED_HOSTS 来让项目支持你期望的ip，例如：
```python
ALLOWED_HOSTS = ['localhost', '192.168.1.3', '192.168.10.2', '127.0.0.1', '*']
```
python网络编程中通常遵循WSGI标准，即由 `client <-> server <-> application` 组成。  
server在其中负责处理http请求，实际的后端功能则由application执行（但server本身也是后端的一部分）。
并且会根据具体的工作情况分配相应进程（也可能是线程？）以方便并行处理多个任务。  
于Django而言，它只提供了简单的server，其重心在application上。 成熟的server框架有：gunicorn、apache、Nginx、uWSGI、etc...</br>

若我们需要创建一个application目录（以下简称app），则可以在命令行中输入:
```cmd
python manage.py startapp [app名]

# 例如说我们创建了一个名为sales的app则可以是：
python manage.py startapp sales
```

## 设置合适的URL请求

随后我们则可以在 `/sales/views.py` 下添加关于http请求的代码，例如：
```python
from django.shortcuts import HttpResponse

def listOrders(request):
    return HttpResponse("以下是订单内容：")
```
之后在 `/[项目名]/urls.py` 中的 urlpatterns 添加路由记录，例如：
```python
from django.contrib import admin
from django.urls import path
from sales.views import listOrders

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sales/orders/', listOrders), 
]
```
此时若服务已启动，则可以在浏览器地址栏中输入 `[指定的ip:端口号]/sales/orders/` 来访问相应目录

也可以通过Django软件包中的 `django.urls.include` 来实现一些简化输入：

```python
"""[项目名]/urls.py"""
from django.urls import path, include
# ⭕在此处添加路由记录
urlpatterns = [
    path('sales/', include('sales.urls')),
]
```
```python
"""sales/urls.py"""
from django.urls import path
from sales.views import listOrders, listOrders2, listOrders3, listOrders4

# ⭕在此处添加路由记录, 此处是sales目录下的路由记录
urlpatterns = [
    path('orders/', listOrders),
    path('orders2/', listOrders2),
    path('orders3/', listOrders3),
    path('orders4/', listOrders4),
]
```
这样就可以让`[项目名]/urls.py`中的输入更为简介一些。

同时也可以用一些正则表达式，可以在Django的官方文档查阅具体示例：https://docs.djangoproject.com/zh-hans/5.1/topics/http/urls/ 
例如：
```python
from django.urls import path
from . import views

urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
]
```

## 让在view.py中的http响应能够返回一个已经写好的网页

### 利用好Django三大件：

#### `from django.shortcuts import HttpResponse, render, redirect`

首先要在 `[项目名]/settings.py` 中修改 `TEMPLATES` 的内容，在 `DIRS` 中添加存放html页面的目录，例如我们用 `htmlFiles`作为目录：
```python
'DIRS': [os.path.join(BASE_DIR, 'htmlFiles')],
```
随后在 `sales\views.py` 中添加一个可以返回html页面的http响应函数（此处默认urls已经写好相应的路由记录）：
```python
from django.shortcuts import render

def mngrOrder(request):
    context = {
        'greetings': '欢迎访问！',
    }
    return render(request, 'mngrTest01.html', context)
```
如果想返回一个现成的网站地址，那么可以用redirect，示例如下：
```python
from django.shortcuts import redirect

def mngrOrder(request):
    return redirect("https://bilibili.com")
```

## 创建数据库

Django默认采用sqlite，输入如下命令可以将创建项目时生成的 db.sqlite3 添加一些简单的表头：
```commandline
python manage.py migrate
```
若需查看数据库，有两种方式：
1. 在PyCharm中安装 Database Navigator 插件，并将 db.sqlite3 添加进 BD Browser 中。
2. 下载安装 SQLiteStudio （ https://github.com/pawelsalawa/sqlitestudio/releases/tag/3.4.17 ）。
