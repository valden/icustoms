from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.BordersListView.as_view(), name='bpoints_list'),
]
