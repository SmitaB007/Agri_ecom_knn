from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
     path('generate_invoice/<int:invoice_id>/',views.invoice_view,name='invoice_view'),
     path('invoice_detail/',views.invoice_detail,name='invoice_detail'),
     path('add_to_wishlist/',views.add_to_wishlist,name='add_to_wishlist'),
     path('view_list/',views.view_list,name="view_list"),
     path('remove_from_wishlist/',views.remove_from_wishlist,name='remove_from_wishlist'),
     path('view_blogs/',views.view_blogs,name="view_blogs"),
     path('create_blog/',views.create_blog,name="create_blog"),
     path('detailed_blog/<int:pk>/',views.detailed_blog,name='detailed_blog'),
     path('list_invoices/',views.list_invoices,name='list_invoices')
]
    