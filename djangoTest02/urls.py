"""
URL 路由设置的入口文件
URL configuration for djangoTest02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sales.views import listOrders

# ⭕在此处添加路由记录
urlpatterns = [
    path('admin/', admin.site.urls),

    path('sales/orders/', listOrders),

    path('sales/', include('sales.urls')),
    path('sales/', include('sales.mngr')),

    path('api/mngr/', include('mngr.urls'))
]  + static("/", document_root="./z_dist")  # 上述路由若没匹配上，则匹配该目录的文件。
