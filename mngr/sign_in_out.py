from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def signin(request):
    # 从POST请求中获取用户名、密码参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 使用Django.contrib.auth里的方法校验用户名、密码
    user = authenticate(username=username, password=password)
    # 若能找到用户且密码正确
    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                request.session['usertype'] = 'mngr'
                return JsonResponse({'ret':0})
            else:
                return JsonResponse({'ret':1, 'msg':'请使用给管理账户登录'})
        else:
            return JsonResponse({'ret':0,'msg':'用户已被禁用'})
    else:
        return JsonResponse({'ret':0, 'msg':'用户或密码错误'})


def signout(request):
    # 直接使用登出方法
    logout(request)
    return JsonResponse({'ret':0})