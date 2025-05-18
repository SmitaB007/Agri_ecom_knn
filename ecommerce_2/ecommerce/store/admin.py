from django.contrib import admin
from .models import Product,Customer,Category,Contact,Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Profile)
admin
class profilemix(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username','first_name','last_name','email']
    inlines = [profilemix]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)