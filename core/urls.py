from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.flatpage, {'url': '/home/'}, name='home'),
    path('contacts/', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
