# Django学习p4：测试后端代码

## 直接配合前端测试

后端的测试可以配合`requests`包构建各种规定的http请求消息来检查响应。  
我们先假设前端已经完成了，并存在`z_dist`目录中。  
需要强调的是，服务这些静态文件不是Django的任务，Django在渲染这些文件的效率很差。故此处的操作仅适用于学习操作。

在 `settings.py` 中，`DEBUG=True` 表示处于调试模式，此时允许Django加载静态网页。并且在 `urls.py` 中的 `urlpatterns` 的末尾加上如下语句：
```python
from django.conf.urls.static import static

urlpatterns = [
    ...
]  + static("/", document_root="./z_dist")  # 上述路由若没匹配上，则匹配该目录的文件。
```
就可以让url通过目录访问对应文件，例如`127.0.0.1/mngr/index.html`

## 使用 `request` 包测试

利用`requests`包的 `post()`、 `get()` 可以模拟提交和获取的行为，

这样就能够借此来测试后端代码。在网站服务启动后，我们可以先用如下代码测试`登录`功能：
```python
import requests, pprint

payloadLogin = {
    'username': 'lanjack',
    'password': '88888888',
}
responseLogin = requests.post('http://127.0.0.1:8000/api/mngr/signin', data=payloadLogin)
pprint.pprint(responseLogin.json())     # 利用pprint来查看返回的消息
```
也可以测试添加信息：
```python
payloadAddCustomer = {
    'action':'add_customer',
    'data':{
        'name':'荒坂工业集团',
        'phonenumber':'114514',
        'address':'夜之城荒坂工业集团大厦'
    }
}
responseAddCustomer = requests.post('http://127.0.0.1:8000/api/mngr/customers', json=payloadAddCustomer)
pprint.pprint(responseAddCustomer.json())
```
``❗❗需要注意的是``：  
因为之前的登录功能是采用Django自带的方法来实现的，故在 `requests.post()` 中使用的是 `data`。  
而增删改查是自己写的方法来操作自己写的表项类，故在 `requests.post()` 中使用的是 `json`。  

而在查找表时，使用的则是 `get()`，并且携带的字段要用 `params`，参考如下：
```python
# 模拟查客户
payloadListCustomer = {
    'action': 'list_customer'
}
responseListCustomer = requests.get('http://127.0.0.1:8000/api/mngr/customers', params=payloadListCustomer)
pprint.pprint(responseListCustomer.json())
```

总之，根据具体的方法、文档具体描述的请求信息，来实现相对应的功能，并以此做测试即可。

## session和token

在每次登录后都会在数据库中的 `django_session` 里保存一行新纪录，这样在后续对网站的操作中，时会先验证当前HTTP请求中头字段的sessionid是否存在于数据库中，
若存在则允许进一步访问，若不存在则按具体要求执行其它操作（例如跳转登录页面）。  
例如我们可以在 `mngr/customers.py` 中 `dispatcher()` 的开头添加如下验证语句：
```python
    # 根据session判断用户是否是登录的管理员
    if 'usertype' not in request.session:
        return JsonResponse(
            {'ret':302, 'msg':'未登录', 'redirect':'/mngr/sign.html'},
            status=302)
    if request.session['usertype'] != 'mngr':
        return JsonResponse(
            {'ret':302, 'msg':'用户不是管理员', 'redirect':'/mngr/sign.html'},
            status=302)
```
这样我们就能对每次的CURD操作进行一个是否登陆过的判断。

为了让验证过程更高效，则会引入一个 token机制。  
比起 `session机制` 是在服务端进行验证——
`token机制` 则是把数据信息直接传给客户端，客户每次请求再携带过来给服务端，服务端无需查询数据库，
直接根据token里面的数据进行验证。
