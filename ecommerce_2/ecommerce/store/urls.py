"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contactus/',views.contact_us,name='contact_us'),
    path('register_user/',views.register_user,name='register_user'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('category/',views.view_category,name='view_category'),
    path('cat_products/<str:fun>/',views.cat_products,name='cat_products'),
    path('view_product/<int:pk>/',views.view_product,name='view_product'),
    path('update_details/',views.update_details,name='update_details'),
    path('update_password/',views.update_password,name='update_password'),
    path('update_info/',views.update_info,name='update_info'),
    path('search/',views.search,name='search'),
    path('orders_invoices/',views.orders_invoices,name='orders_invoices'),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('without_login_update_password/<str:email>/',views.without_login_update_password,name="without_login_update_password")
]
