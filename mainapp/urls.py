from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('category/<int:pk>', mainapp.products, name='category'),
    path('category/<int:pk>/<page>/', mainapp.products, name='page'),
    path('product/<int:pk>', mainapp.product, name='product'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
