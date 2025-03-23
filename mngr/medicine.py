from django.http import JsonResponse
import json

import json

from django.http import JsonResponse

from common.models import Medicine


def dispatcher(request):
    """将请求参数同意放入request的params属性中，方便后续处理"""
    """下述接口接口均来自：https://www.byhy.net/py/django/doc_api_v1_0/"""

    # # 根据session判断用户是否是登录的管理员
    # if 'usertype' not in request.session:
    #     return JsonResponse(
    #         {'ret':302, 'msg':'未登录', 'redirect':'/mngr/sign.html'},
    #         status=302)
    # if request.session['usertype'] != 'mngr':
    #     return JsonResponse(
    #         {'ret':302, 'msg':'用户不是管理员', 'redirect':'/mngr/sign.html'},
    #         status=302)

    # GET请求参数在requests对象的GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE请求参数从request对象的body属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)   # 根据接口，此三种属性请求的消息体都是JSON格式。故此处将其变为python的对象

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_medicine':
        return listMedicine(request)
    elif action == 'add_medicine':
        return addMedicine(request)
    elif action == 'modify_medicine':
        return modifyMedicine(request)
    elif action == 'del_medicine':
        return deleteMedicine(request)

    else:
        return JsonResponse({'ret':1, 'msg': '不支持的HTTP请求类型'})


def listMedicine(request):
    qs = Medicine.objects.values()
    retList = list(qs)      # 将Query对象转为list类型，否则无法被转换为JSON字符串
    return JsonResponse({'ret':0, 'retlist':retList})


def addMedicine(request):
    info = request.params['data']   # 从发送来的请求中提取 'data' 的内容
    record = Medicine.objects.create(
        desc=info['desc'],
        name=info['name'],
        sn=info['sn'],
    )
    return JsonResponse({'ret':0, 'id':record.id,})


def modifyMedicine(request):
    medicineID = request.params['id']
    newData = request.params['newdata']
    # 此处需对提交内容判定是否合法
    try:
        medicine = Medicine.objects.get(id=medicineID)
    except Medicine.DoesNotExist:
        return {
            'ret':1,
            'msg': f'id为`{medicineID}`的客户不存在'
        }
    if 'name' in newData: medicine.name = newData['name']
    if 'desc' in newData: medicine.desc = newData['desc']
    if 'sn' in newData:medicine.sn = newData['sn']
    medicine.save()     # 保存到数据库中
    return JsonResponse({'ret':0})


def deleteMedicine(request):
    MedicineID = request.params['id']
    try:
        medicine = Medicine.objects.get(id=MedicineID)
    except:
        return {
            'ret':1,
            'msg':f'ID为`{MedicineID}`的客户不存在'
        }
    medicine.delete()   # 从数据库中删除
    return JsonResponse({'ret':0})
