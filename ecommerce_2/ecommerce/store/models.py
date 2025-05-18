from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(max_length=20)
    address1 = models.CharField(max_length=20)
    address2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=200,blank=True)
    state = models.CharField(max_length=50,blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=10,blank=True)
    old_cart = models.CharField(max_length=500,blank=True,null=True,default="{}")
    
    def __str__(self):
        return self.user.username
    
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile,sender=User)







class Category(models.Model):
    name = models.CharField(max_length=50)
    tax = models.DecimalField(default=5,decimal_places=2,max_digits=4)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name - self.last_name}'
    

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/products/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    delivery_charges = models.DecimalField(default=40,decimal_places=2,max_digits=4)
    in_stock = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    


    
class Contact(models.Model):
    email = models.EmailField(max_length=50)
    message = models.CharField(max_length=250)

    def __str__(self):
        return self.email
    



