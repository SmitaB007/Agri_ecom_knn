from django.shortcuts import render,redirect,get_object_or_404
from cart.cart import Cart
from store.models import Profile,Product
from payment.models import ShippingAddress,Order,OrderItem,UserPurchase
from django.contrib.auth.models import User
from .forms import shipping_form,paymentform
from store.forms import Update_info
from django.contrib import messages
# from .utils import generate_invoice
from django.http import HttpResponse
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from invoice.models import user_inv
import uuid
import base64
from .utils import get_recommendation
import qrcode
from django.http import HttpResponse,JsonResponse
from io import BytesIO
import stripe
from django.conf import settings
import time
from django.urls import reverse
from django.core.mail import send_mail,EmailMessage


#   
#   
# Create your views here.


@receiver(post_save,sender=Order)
def send_email_on_change(sender,instance,created,**kwargs):
    
    if instance.is_paid:
       try:
        subject = "Order confirmation"
        message = f"Dear,{instance.user.username},Your payment has been received,and order will arrive within 2-3 days.Thank you for shopping with sai-krupa agrotech!"
        recipient_list = [instance.user.email]
        doc = user_inv.objects.filter(user=instance.user)
        document = doc[len(doc)-1]
    
        doc_path = document.pdf_file.path
        email = EmailMessage(
           subject=subject,
           body=message,
           from_email = settings.EMAIL_HOST_USER,
           to = [instance.user.email]
        )
        with open(doc_path,"rb") as pdf_file:
           email.attach(document.pdf_file.name,pdf_file.read(),"application/pdf")
        email.send(fail_silently=False)
        return "Email sent successfully!"
    
       except doc.DoesNotExist:
               return "file not found"

def recom_prod(userid):
      prod_ids = get_recommendation(userid)
      prods = Product.objects.filter(id__in=prod_ids)
      
      return prods

def payment_success(request):
    return render(request,'success.html',{})

def payment_failure(request):
    return render(request,'failure.html',{})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    cart_qty = cart.get_qty()
    amount,tax,delivery = cart.get_amount()
    amount = round(amount)

    return render(request,'checkout.html',{'cart_products':cart_products,'cart_qty':cart_qty,'amount':amount,'tax':tax,'delivery':delivery})

def billing(request):
    print("function billing")
    if request.user.is_authenticated:
        shipping_user,created = ShippingAddress.objects.get_or_create(user=request.user,defaults={
                         'shipping_fullname':'',
                         'shipping_Address1' :'',
                         'shipping_email':'',
                         'shipping_zipcode':'',
                         'shipping_state':'',
        })
        cu = User.objects.get(id=request.user.id)
        
        shippingform = shipping_form(request.POST or None,instance=shipping_user)
        
        if  shippingform.is_valid():
             shippingform.save()
            #  myship = request.POST
            #  request.session['myship'] = myship
             messages.success(request,f'{cu.first_name}\'s personal info has been updated ')
             
        return render(request,'billing.html',{'shippingform':shippingform})
        


def billing_process(request):
    
    if request.POST:
     userid = request.user.id
     cart = Cart(request)
     cart_products = cart.get_prods()
     cart_qty = cart.get_qty()
     amount,tax,delivery = cart.get_amount()
     amount = round(amount)
     my_shipping = request.POST
     request.session['my_shipping'] = my_shipping
     print(my_shipping)
     for l in cart_products:
        product_id = l.id
        for k,v in cart_qty.items():
          key = int(k)
          if key == l.id:
             pro = Product.objects.get(id=product_id)
             purch = UserPurchase(user=request.user,product=pro)
             purch.save()
             print("purchase saved")
     
     products = recom_prod(userid)
     print(len(products))
     if request.user.is_authenticated:
       return render(request,'billing_process.html',{'cart_products':cart_products,'cart_qty':cart_qty,'shippingform':request.POST,'amount':amount,'products':products,'tax':tax,'delivery':delivery})
         
     else:
         pass
     shipping_form = request.POST
     return render(request,'billing_process.html',{'cart_products':cart_products,'cart_qty':cart_qty,'shippingform':shipping_form})
    else:
        messages.success(request,"access denied")
        redirect('home')


def order_process(request,method):
    my_shipping = request.session.get('my_shipping')
   
    cart = Cart(request)
    cart_products = cart.get_prods()
    cart_qty = cart.get_qty()  
    amount,tax,delivery = cart.get_amount()
    fullname = my_shipping['shipping_fullname']
    email = my_shipping['shipping_email']
    amount_paid = int(amount)
    shipping_address = f"{my_shipping['shipping_fullname']}\n{my_shipping['shipping_email']}\n{my_shipping['shipping_Address1']}"
     
    if request.user.is_authenticated:
     user = request.user
     c_order = Order(user=user,full_name=fullname,email=email,Shipping_address=shipping_address,amount_paid=amount_paid,payment_method=method)
     c_order.save()
     print("in order process")

     order_id = c_order.pk
     for l in cart_products:
        product_id = l.id
        if l.is_sale:
           price = l.sale_price
        else:
           price = l.price
        
        for k,v in cart_qty.items():
          key = int(k)
          if key == l.id:
             order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=v,price=price)
             order_item.save()
             print(order_item)
             

    

     for key in list(request.session.keys()):
        if key == "session_key":
           del request.session[key]
      
     current_user = Profile.objects.filter(user__id =request.user.id)
     current_user.update(old_cart="")
     
     
     messages.success(request,'Order placed')
     return redirect('home')

    else:
     return redirect('home')
    


def shipped_products(request):
   if request.user.is_authenticated and request.user.is_superuser:
     orders = Order.objects.filter(is_shipped=True)
     return render(request,"shipped.html",{"orders":orders})
   else:
    messages.success(request,'access denied')
    return redirect('home')

def not_shipped_products(request):
   if request.user.is_authenticated and request.user.is_superuser:
     orders = Order.objects.filter(is_shipped=False)
     return render(request,"not_shipped.html",{"orders":orders})
   else:
    messages.success(request,'access denied')
    return redirect('home')


def detailed_view(request,pk):
   if request.user.is_authenticated and request.user.is_superuser:
     orders = Order.objects.get(id=pk)
     products = OrderItem.objects.filter(order=pk)
     return render(request,"detailed_view.html",{"orders":orders,'products':products})
   else:
    messages.success(request,'access denied')
    return redirect('home')

def payment_process(request):
   if request.POST:
      form = paymentform(request.POST or None)

   else:
      messages.success(request,"access denied")
      return redirect('home')
   
def payment_view(request):


  cart = Cart(request)
  total = cart.get_amount()
  
 
   
  

  if request.user.is_authenticated:
  
    payment_form = paymentform()

    return render(request,"payment_form.html",{'payment_form':payment_form})
  
      
    

def generate_qr(request,total):
    
    upi_id = "smitabhoine2007@okhdfcbank"
    payee_name = "Sai-krupa agrotech"
    note = "Payment for Order #123"
    amount = int(float(total)*100)
    # intent = stripe.PaymentIntent.create(
    #    amount = amount,
    #    currency="inr",
    #    payment_method_types=["upi"],
    # )

    
    
    upi_link = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount/100}&cu=INR&tn={note}"

   
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")



def pay_now(request,method):
   cart = Cart(request)
   amount,tax,delivery = cart.get_amount()
   amount= int(amount)
   return render(request,"qr.html",{"amount":amount,"method":method})

def selection(request):
    if request.method == "POST":
       choice = request.POST.get("choice")
       if choice == "COD":
         return redirect(reverse('order_process',kwargs={'method':'COD'}))
       if choice == "QR":
         return redirect (reverse('pay_now',kwargs={'method':'QR Code'}))

    return render(request,"selection.html",{})

def order_shipped(request,oid):
    if request.user.is_authenticated and request.user.is_superuser:
     orders = Order.objects.get(id=oid)
     orders.is_shipped = True
     orders.save()
     return redirect('shipped_products')
    
def order_paid(request,sid):
     if request.user.is_authenticated and request.user.is_superuser:
       orders = Order.objects.get(id=sid)
       orders.is_paid = True
       orders.save()
       return redirect('list_invoices')   



           
