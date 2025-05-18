from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime
from uuid import uuid4
# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    shipping_fullname = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=100)
    shipping_Address1 = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100,default="")


    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'shipping add - {str(self.user.id)}'








class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=30)
    Shipping_address =  models.TextField(max_length=13000)
    amount_paid = models.DecimalField(max_digits=6,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100,blank=True,default="")

    def __str__(self):
       return f'order of {self.full_name}'


@receiver(pre_save,sender=Order)
def set_shipped_date(sender,instance,**kwargs):
   if instance.pk:
       current = datetime.datetime.now()
       obj = sender._default_manager.get(pk=instance.pk)
       if instance.is_shipped and not obj.is_shipped:
           instance.date_shipped = current


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return f'orderitems of {self.user.id}'
    

class UserPurchase(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}\'s products'  



