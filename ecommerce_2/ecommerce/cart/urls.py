from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.summary,name='cart_summary'),
    path('add/',views.cart_add,name='cart_add'),
    path('delete/',views.cart_delete,name='cart_delete'),
    path('update/',views.update_prod,name='update_prod')
]