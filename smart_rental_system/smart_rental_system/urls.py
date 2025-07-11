"""smart_rental_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include
from machinery import views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('admin-dashboard',views.admin_dashboard,name="admin_dashboard"),
    path("my-rentals",views.my_rentals,name="my_rentals"),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('equipments-list',views.equipment_list,name="equipment_list"),
    path('renter-equipument/',views.renter_equipument,name="renter-equipument"),
    path('update-machinery/<int:equipment_id>/',views.update_machinery,name="update_machinery"),
    path('delete_machinery/<int:equipment_id>/',views.delete_machinery,name="delete-machinery")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
