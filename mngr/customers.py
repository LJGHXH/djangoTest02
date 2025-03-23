import json

from django.http import JsonResponse

from common.models import Customer


def dispatcher(request):
    """将请求参数同意放入request的params属性中，方便后续处理"""
    """下述接口接口均来自：https://www.byhy.net/py/django/doc_api_v1_0/"""

    # 根据session判断用户是否是登录的管理员
    if 'usertype' not in request.session:
        return JsonResponse(
            {'ret':302, 'msg':'未登录', 'redirect':'/mngr/sign.html'},
            status=302)
    if request.session['usertype'] != 'mngr':
        return JsonResponse(
            {'ret':302, 'msg':'用户不是管理员', 'redirect':'/mngr/sign.html'},
            status=302)

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


def listCustomer(request):
    qs = Customer.objects.values()
    retList = list(qs)      # 将Query对象转为list类型，否则无法被转换为JSON字符串
    return JsonResponse({'ret':0, 'retlist':retList})


def addCustomer(request):
    info = request.params['data']   # 从发送来的请求中提取 'data' 的内容
    print("info: ", info, "\ntype: ", type(info))
    record = Customer.objects.create(
        name=info['name'],
        phoneNumber=info['phonenumber'],
        address=info['address'],
    )
    return JsonResponse({'ret':0, 'id':record.id,})


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
