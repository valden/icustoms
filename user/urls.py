from django.urls import path, include
from . import views


urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/documents/', views.DocumentListView.as_view(),
         name='profile_documents'),
    path('profile/documents/create/', views.DocumentCreateView.as_view(),
         name='profile_document_create'),
    path('profile/documents/<int:pk>/', views.DocumentUpdateView.as_view(),
         name='profile_document_update'),
    path('profile/documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(),
         name='profile_document_delete'),
    path('profile/vehicles/', views.VehicleListView.as_view(),
         name='profile_vehicles'),
    path('profile/vehicles/create/', views.VehicleCreateView.as_view(),
         name='profile_vehicle_create'),
    path('profile/vehicles/<int:pk>/', views.VehicleUpdateView.as_view(),
         name='profile_vehicle_update'),
    path('profile/vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(),
         name='profile_vehicle_delete'),
]
