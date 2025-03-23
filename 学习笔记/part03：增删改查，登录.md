# Django学习p3：增删改查，登录

## 增删改查

对数据库的增删改查实质上是根据不同的前端请求来进行各种操作。前端以request形式描述具体内容，通常这些内容会在开发文档中规定清楚。
而后端也就需要根据文档来写具体功能了。  

先前我们都是在 `view.py` 中编写，但所有功能都在那里面实现的话会非常复杂。故在此处创建一个 `customers.py` ，在这里面协具体功能。 

对于这个练习项目，API参考文档：https://www.byhy.net/py/django/doc_api_v1_0/

根据文档内容，增删改查均指向同一个url，故可以根据`request`中的`ACTION`来判定具体的操作。代码如下：
```python
"""mngr/customers.py"""
import json
from django.http import JsonResponse

def dispatcher(request):
    """将请求参数统一放入request的params属性中，方便后续处理"""

    # GET请求参数在requests对象的GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE请求参数从request对象的body属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)   # 根据接口，此三种属性请求的消息体都是JSON格式。故此处将其变为python的对象

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return listCustomer(request)
    elif action == 'add_customer':
        return addCustomer(request)
    elif action == 'modify_customer':
        return modifyCustomer(request)
    elif action == 'del_customer':
        return deleteCustomer(request)

    else:
        return JsonResponse({'ret':1, 'msg': '不支持的HTTP请求类型'})
```

### 查
```python
def listCustomer(request):
    qs = Customer.objects.values()
    retList = list(qs)      # 将Query对象转为list类型，否则无法被转换为JSON字符串
    return JsonResponse({'ret':0, 'retlist':retList})

```

### 增
```python
def addCustomer(request):
    info = request.params['data']   # 从发送来的请求中提取 'data' 的内容
    record = Customer.objects.create(
        name=info['name'],
        phoneNumber=info['phonenumber'],
        address=info['address'],
    )
    return JsonResponse({'ret':0, 'id':record.id,})
```

### 改
```python
def modifyCustomer(request):
    customerID = request.params['id']
    newData = request.params['newdata']
    # 此处需对提交内容判定是否合法
    try:
        customer = Customer.objects.get(id=customerID)
    except Customer.DoesNotExist:
        return {
            'ret':1,
            'msg': f'id为`{customerID}`的客户不存在'
        }
    if 'name' in newData: customer.name = newData['name']
    if 'phonenumber' in newData: customer.phoneNumber = newData['phonenumber']
    if 'address' in newData:customer.address = newData['address']
    customer.save()     # 保存到数据库中
    return JsonResponse({'ret':0})
```

### 删
```python
def deleteCustomer(request):
    customerID = request.params['id']
    try:
        customer = Customer.objects.get(id=customerID)
    except:
        return {
            'ret':1,
            'msg':f'ID为`{customerID}`的客户不存在'
        }
    customer.delete()   # 从数据库中删除
    return JsonResponse({'ret':0})
```

需要注意的是，Django会默认开启CSRF安全防护机制（它要求所有POST、PUT类型的请求都必须在HTTP请求头中携带用于校验的数据。
处于练习的简便，我们`暂时`在`settings.py`里的`MIDDLEWARE`变量中的`'django.middleware.csrf.CsrfViewMiddleware'`注释掉，临时取消掉。

## 登录、登出

登录、登出功能可以直接用Django的 `django.contrib.auth` 里的 `login`、`logout` 实现，同时配合 `authenticate` 来对用户名和密码进行校验。  

登录功能参考如下：
```python
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

def signin(request):
    # 从POST请求中获取用户名、密码参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 使用Django.contrib.auth里的authenticate方法校验用户名、密码
    user = authenticate(username=username, password=password)
    # 若能找到用户且密码正确
    if user is not None:
        # 下述两项if是来自于数据库
        if user.is_active:
            if user.is_superuser:
                login(request, user)    # 使用Django的login()登录
                request.session['usertype'] = 'mngr'
                return JsonResponse({'ret':0})
            else:
                return JsonResponse({'ret':1, 'msg':'请使用给管理账户登录'})
        else:
            return JsonResponse({'ret':0,'msg':'用户已被禁用'})
    else:
        return JsonResponse({'ret':0, 'msg':'用户或密码错误'})
```

登出功能参考如下：
```python
def signout(request):
    # 直接使用登出方法
    logout(request)
    return JsonResponse({'ret':0})
```

