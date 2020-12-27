from django.urls import path, re_path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.login, name='logout'),
]
