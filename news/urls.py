# news/urls.py

from django.urls import path
from . import views


urlpatterns = [
    # News patterns
    path('', views.NewsListView.as_view(), name='news_list'),
]
