from django.contrib import admin
from django.urls import path
from sales.views import listOrders, listOrders2, listOrders3, listOrders4, listCustomer, listCustomer2

# ⭕在此处添加路由记录, 此处是sales目录下的路由记录
urlpatterns = [

    path('admin/', admin.site.urls),

    path('orders/', listOrders),
    path('orders2/', listOrders2),
    path('orders3/', listOrders3),
    path('orders4/', listOrders4),

    path('customer/', listCustomer),
    path('customer_tutorial/', listCustomer2),
]
