from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    cart_qty = cart.get_qty()
    amount,tax,delivery = cart.get_amount()
    
    amount = round(amount)
    return render(request,'cart_summary.html',{'cart_products':cart_products,'cart_qty':cart_qty,'amount':amount,'tax':tax,'delivery':delivery})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        print(product_id)
        product = get_object_or_404(Product,id=product_id)
        product_qty = int(request.POST.get('product_qty'))
        cart.add(product=product,quantity=product_qty)
        messages.success(request,"Product added to cart")
        cart_quantity = cart.__len__()
        response = JsonResponse({'quantity':cart_quantity})
        
        return response
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete_prod(product=product_id)
        messages.success(request,"Product removed from cart")
        response = JsonResponse({'id':product_id})
        return response
    
def update_prod(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=product_qty)
        messages.success(request,"order updated")
        response = JsonResponse({'id':product_id})
        return response
