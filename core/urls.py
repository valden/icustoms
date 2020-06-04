from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.flatpage, {'url': '/home/'}, name='home'),
    path('contacts/', include('contacts.urls')),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('cabinet/', views.flatpage, {'url': '/cabinet/'}, name='cabinet'),
    path('calcs/', views.flatpage, {'url': '/calcs/'}, name='calcs'),
    path('maps/', views.flatpage, {'url': '/maps/'}, name='maps'),
    path('uktzed/', views.flatpage, {'url': '/uktzed/'}, name='uktzed'),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('news/', include('news.urls')),
    path('forum/', include('posts.urls')),
    path('declaring/', include('declaring.urls')),
    path('deskbooks/', include('deskbooks.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
