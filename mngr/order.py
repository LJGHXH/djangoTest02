from django.db import IntegrityError, transaction
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
