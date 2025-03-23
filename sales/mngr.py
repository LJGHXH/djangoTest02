from django.urls import path
from sales.views import mngrOrder, mngrOrder2, mngrOrder3, mngrOrder4

# ⭕在此处添加路由记录, 此处是sales目录下的路由记录
urlpatterns = [
    path('mngr/', mngrOrder, name='index'),
    path('mngr2/', mngrOrder2),
    path('mngr3/', mngrOrder3),
    path('mngr4/', mngrOrder4, name='index'),
]