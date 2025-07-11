from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'machinery'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('renter-dashboard/', views.renter_dashboard, name='renter_dashboard'),
    path('equipment/', views.available_equipment, name='available_equipment'),
    path('add-machinery/', views.add_machinery, name='add_machinery'),
    path('request-rental/<int:machinery_id>/', views.request_rental, name='request_rental'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('update-machinery/',views.update_machinery),
    path('renter-equipument/',views.renter_equipument,name="renter-equipument")
]
