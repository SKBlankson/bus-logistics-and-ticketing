"""
URL configuration for AshesiLogisticsAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from .views import driver_endpoints

urlpatterns = [
    path('drivers/',driver_endpoints.get_driver),
    path('drivers/alldrivers', driver_endpoints.get_all_drivers),
    path('drivers/newdriver', driver_endpoints.create_new_driver),
    path('drivers/updatedriver', driver_endpoints.update_driver_details),
    path('drivers/deletedriver', driver_endpoints.delete_driver),
]
