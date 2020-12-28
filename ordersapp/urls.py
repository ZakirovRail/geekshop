from django.urls import path, re_path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='orders_list'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='order_create'),
    path('read/<int:pk>', ordersapp.OrderDetailView.as_view(), name='order_read'),
    path('edit/<int:pk>', ordersapp.OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>', ordersapp.OrderDeleteView.as_view(), name='order_delete'),
    path('complete/<int:pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
]

# urlpatterns = [
#     re_path(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
#     # re_path(r'^forming/complete/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='order_forming_complete'),
#     re_path(r'^create/$', ordersapp.OrderCreateView.as_view(), name='order_create'),
#     # re_path(r'^read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
#     # re_path(r'^update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
#     # re_path(r'^delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),
# ]
