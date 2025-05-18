from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
 path('payment_success/',views.payment_success,name='payment_success'),
 path('payment_failure/',views.payment_failure,name='payment_failure'),
 path('checkout/',views.checkout,name='checkout'),
 path('billing/',views.billing,name='billing'),
 path('billing_process/',views.billing_process,name='billing_process'),
 path('order_process/<str:method>/',views.order_process,name='order_process'),
 path('shipped_products/',views.shipped_products,name='shipped_products'),
 path('not_shipped_products/',views.not_shipped_products,name='not_shipped_products'),
 path('orders/<int:pk>',views.detailed_view,name='detailed_view'),
 path('payment_view/',views.payment_view,name='payment_view'),
 path('pay_now/<str:method>/',views.pay_now,name="pay_now"),
 path('generate_qr/<int:total>/',views.generate_qr,name="generate_qr"),
 path('selection/',views.selection,name='selection'),
 path('track/<int:oid>/',views.order_shipped,name="order_shipped"),
 path('order_paid/<int:sid>/',views.order_paid,name="order_paid")

 # path('verify_payment/<str:payment_intent_id>/',views.verify_payment,name='verify_payment')
 # path('stripe/webhook/',views.stripe_webhook,name='stripe_webhook')
]
