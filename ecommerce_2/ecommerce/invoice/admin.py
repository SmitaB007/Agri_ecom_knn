from django.contrib import admin
from .models import user_inv,wishlist,product_review,blog
# Register your models here.
admin.site.register(user_inv)
admin.site.register(wishlist)
admin.site.register(product_review)
admin.site.register(blog)


