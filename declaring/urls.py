from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('create/', views.EntryCreateView.as_view(),
         name='entry_create'),
    path('entry/<int:pk>/', views.EntryUpdateView.as_view(),
         name='entry_update'),
    path('entry/<int:pk>/preview/', views.EntryPreView.as_view(),
         name='entry_preview'),
    path('entry/<int:pk>/print/', views.EntryPrintView.as_view(),
         name='entry_print'),
    path('entry/<int:pk>/email/', views.EntrySendEmail.as_view(),
         name='entry_email'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(),
         name='entry_delete'),


    # path('profile/vehicles/', views.VehicleListView.as_view(),
    #      name='profile_vehicles'),
    # path('profile/vehicles/create/', views.VehicleCreateView.as_view(),
    #      name='profile_vehicle_create'),
    # path('profile/vehicles/<int:pk>/', views.VehicleUpdateView.as_view(),
    #      name='profile_vehicle_update'),
    # path('profile/vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(),
    #      name='profile_vehicle_delete'),
]
