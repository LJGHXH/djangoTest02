"""通常会在里面写关于http请求的代码"""

# Django三大件
from django.shortcuts import HttpResponse, render, redirect
from django.template import loader

from common.models import Customer

import datetime

# Create your views here.


def listOrders(request):
    return HttpResponse("以下是订单内容：")


def listOrders2(request):
    return HttpResponse("以下是订单内容2：")


def listOrders3(request):
    return HttpResponse("以下是订单内容3：")


def listOrders4(request):
    return HttpResponse("以下是订单内容4：")


def mngrOrder(request):
    context = {
        'greetings': '欢迎访问！',
        'current_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render(request, 'mngrTest01.html', context)


def mngrOrder2(request):
    return HttpResponse("我是管理员2：")


def mngrOrder3(request):
    return redirect('https://bilibili.com')


def mngrOrder4(request):
    context = {
        'greetings': '欢迎访问！',
        'current_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render(request, 'PHP_LibraryManage/d1_SignUp.php', context)


def listCustomer(request):
    # type(qs) = <QuerySet>，其包含读取到的所有记录。每条记录都是一个dict对象（key是字段名，value是字段值）
    qs = Customer.objects.values()      # objects 来自 models.Model

    # 根据url中的phoneNumber查询
    pn = request.GET.get('phonenumber', None)   # 注意，url在浏览器刷新时会自动全转为小写，所以此处冒号内不要出现大写
    if pn:
        qs = qs.filter(phoneNumber=pn)

    # 定义返回字符串
    retStr = ''
    for customer in qs:
        retStr += '<tr>'
        for name, value in customer.items():
            retStr += f'<td> {value} </td>'
        retStr += '</br>'
    customer_template = loader.get_template('customerTemplate.html')    # 以模板形式(Django的Template)获取html文件
    customer_template = customer_template.render()      # 将模板转换为字符串形式(Django的SafeString)

    return HttpResponse(customer_template%retStr)


def listCustomer2(request):
    qs = Customer.objects.values()

    # 根据url中的phoneNumber查询
    pn = request.GET.get('phonenumber', None)
    if pn:
        qs = qs.filter(phoneNumber=pn)


    with open("D:/CODE/Python/WebCoding/djangoTest02/htmlFiles/customerTemplateTutorial.html", "r", encoding="utf-8") as file:
        customer_template = file.read()

    from django.template import engines
    django_engine = engines['django']
    template = django_engine.from_string(customer_template)

    rendered = template.render({'customers':qs})
    return HttpResponse(rendered)

