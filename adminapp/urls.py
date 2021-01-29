from django.urls import path, re_path

import adminapp.views as adminapp


app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    path('users/update/<pk>', adminapp.user_update, name='user_update'),
    path('users/delete/<pk>', adminapp.user_delete, name='user_delete'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/update/<int:pk>', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    re_path(r'^products/create/category/(?P<pk>\d+)/$', adminapp.ProductCreateView.as_view(), name='product_create'),
    re_path(r'^products/read/category/(?P<pk>\d+)/$', adminapp.ProductListView.as_view(), name='products'),
    path('products/read/<pk>', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<pk>', adminapp.product_update, name='product_update'),
    re_path(r'^products/delete/(?P<pk>\d+)/$', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]
