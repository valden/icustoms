# posts/urls.py

from django.urls import path, include
from . import views


urlpatterns = [
    # Topics' patterns
    path('', views.TopicListView.as_view(), name='topic_list'),
    path('new/', views.TopicCreateView.as_view(), name='topic_new'),
    path('<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_edit'),
    path('<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    # Posts' patterns
    path('<int:topic>/posts/', views.PostListView.as_view(), name='post_list'),
    path('<int:topic>/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:topic>/posts/<int:pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('<int:topic>/posts/new/', views.PostCreateView.as_view(), name='post_new'),
    path('<int:topic>/posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
