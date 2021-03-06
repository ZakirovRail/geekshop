from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path

from mainapp import views as mainapp


urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    # path('subadmin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
   re_path(r'^order/', include('ordersapp.urls', namespace='order')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
    import debug_toolbar

    # urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    # urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
