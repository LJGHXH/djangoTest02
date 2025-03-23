# Django学习p0：后端知识储备

搞好数据库：查询语句的优化很重要，做好必要的分表分库。</br>

## 缓存redis

一个开源的键值存储系统，用作数据库、缓存、消息代理。若需要配置Django来使用redis，需要先pip安装 `django-redis` 包。  
随后在Django的设置中配置缓存，例如：
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

## 鉴权JWT

一个基于JSON的开放标准，用于在网络应用环境间传递声明。  
在Django中常用于实现无状态的认证机制，Django中实现jwt的方式是用 `djangorestframework-simplejwt` 包。  

安装完后需要在 `settings.py` 配置：
在 `INSTALLED_APPS` 中添加 `'rest_framework_simplejwt'` , 
在 `REST_FRAMEWORK` 中设置默认认证类为 `'rest_framework_simplejwt.authentication.JWTAuthentication'`。  

获取JWT令牌在`urls.py`中的路由配置如下：
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/token/', 
         TokenObtainPairView.as_view(),
         name='token_obtain_pair', 
    )
]
```

## 特殊接口限流：例如注册请求。  

## 日志记录：接口请求记录。  

## 接口文档可以用swagger生成

Swagger可以快速构建和文档化API。
通过描述API的路径、参数、请求体、响应、错误码等信息使API设计简单易懂。

在Django项目中可用 `drf-yasg2` 包来生成Swagger文档。  
在 `settings.py` 中添加 'drf_yasg2' 到 `INSTALLED_APPS` 中。
在 `urls.py` 中设置 `schema_view` ：
```python
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tweet API",
        default_version='v1',
        description="Welcome to the world of Tweet",
        terms_of_service="https://www.tweet.org",
        contact=openapi.Contact(email="demo@tweet.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('polls/', include('polls.urls')),
    path('tweet/', include('tweets.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace="api-auth")),
]
```
