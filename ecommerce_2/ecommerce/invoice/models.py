from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_inv(models.Model):
    invoice_number = models.CharField(max_length=20,unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="invoices/",blank=True,null=True)
    order = models.ForeignKey('payment.Order',on_delete=models.CASCADE,blank=True,null=True)
    items = models.ManyToManyField('payment.OrderItem',blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f'invoice of {self.invoice_number}'


class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username}\'s wishlist'


class product_review(models.Model):
    product = models.ForeignKey('store.Product',on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    rating = models.IntegerField()
    review = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.user.username}\'s review for {self.product.name}'
    

class blog(models.Model):
    content = models.TextField(max_length=10000)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='uploads/blog_img/',default="")

    def __str__(self):
        return f'blog of {self.user.username}'
    
