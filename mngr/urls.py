from django.urls import path
from mngr import customers, medicine, sign_in_out, order

# ⭕在此处添加路由记录, 此处是mngr目录下的路由记录
urlpatterns = [
    path('customers', customers.dispatcher),
    path('medicines', medicine.dispatcher),
    path('orders', order.dispatcher),

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout)
]
