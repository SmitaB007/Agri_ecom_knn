from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem,UserPurchase
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class ordermix(admin.StackedInline):
    model = OrderItem
    extra = 0

class orderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['full_name','email','Shipping_address','amount_paid','is_shipped','date_shipped','payment_method','is_paid']
    inlines = [ordermix]

admin.site.unregister(Order)
admin.site.register(Order,orderAdmin)
admin.site.register(UserPurchase)
