from django.shortcuts import render,redirect,get_object_or_404
from invoice.forms import Reviewform
from invoice.models import product_review
from .models import Product,Category,Profile
from .forms import contactus,SignUpForm,Update_details,Update_password,Update_info
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from django.db.models import Q
import json
from payment.forms import shipping_form
from payment.models import ShippingAddress
from cart.cart import Cart
import google.generativeai as genai
from ecommerce import settings
from invoice.models import product_review
from django.core.mail import send_mail,EmailMultiAlternatives

# Create your views here.

def get_response(input):
   genai.configure(api_key=settings.genai_api_key)
   model = genai.GenerativeModel('gemini-1.5-flash')
   response = model.generate_content(input)
   return response.text



 
def home(request):
    prod = Product.objects.all()[:6]
    reviews = product_review.objects.all()
    user_ques = None
    bot_answer = None

    if request.method == "POST":
      user_ques = request.POST.get('question')

      if user_ques:
         bot_answer = get_response(user_ques)

    
    return render(request,'home.html',{'prod':prod,'bot_answer':bot_answer,'user_ques':user_ques,'reviews':reviews})

def about(request):
    return render(request,'about.html',{})

def contact_us(request):
    form = contactus(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request,"Message sent successfully")
        return redirect('home')
    return render(request,'contactus.html',{'form':form})

def view_category(request):
    cat = Category.objects.all()
    return render(request,'category.html',{'cat':cat})

def cat_products(request,fun):
    try:
        cat = Category.objects.get(name=fun)
        prod = Product.objects.filter(category=cat)
        return render(request,'category_products.html',{'prod':prod})
    except:
        messages.success(request,"error")
        return redirect('home')
    
def view_product(request,pk):
    product = Product.objects.get(id=pk)
    product_new = get_object_or_404(Product,id=pk)
    prods = product_review.objects.filter(product=product_new)
    form = Reviewform()
    if request.user.is_authenticated:
      if request.method == "POST":
         form = Reviewform(request.POST)
         if form.is_valid() :
            review = form.save()
            review.product = product_new
            review.user = request.user
            review.save()
            print("submitted")
            return redirect('view_product',pk=product_new.id)
    else:
         form = Reviewform()

    return render(request,'view_product.html',{'product':product,'form':form,'prods':prods})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"User registered")
            return redirect('update_info')
        else:
            messages.success(request,"please,fill the info once again")
            return redirect('register_user')
    else:
        return render(request,'register.html',{'form':form})


   

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None : 
            login(request,user)
            current_user = Profile.objects.get(user__id=request.user.id)
            savedcart = current_user.old_cart
            print(savedcart)
            #str to dictionary
            if savedcart:
                
                converted_cart = json.loads(savedcart)
                print(converted_cart)
                cart = Cart(request)
                #{"2":2,"1":2}
                for k,v in converted_cart.items():
                    cart.db_add(product=k,quantity=v)

            messages.success(request,"user logged in")
            return redirect('home')
        else:
            messages.success(request,"error in logging in")
            return redirect('login_user')
    else:
        return render(request,"login_user.html",{})
    

def logout_user(request):
    logout(request)
    messages.success(request,"user logged out")
    return redirect('home')


def update_details(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        userform = Update_details(request.POST or None,instance=current_user)

        if userform.is_valid():
            userform.save()
            login(request,current_user)
            messages.success(request,f'{current_user.first_name}\'s details has been updated ' )
            return redirect('home')
        return render(request,'update_user.html',{'userform':userform})
    else:
        messages.success(request,"user needs to registered first")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == "POST":
           userform = Update_password(current_user,request.POST)
           if userform.is_valid():
              userform.save()
              login(request,current_user)
              messages.success(request,f'{current_user.first_name}\'s password has been updated ' )
              return redirect('home')
           else:
              messages.success(request,"error in changing password" )
        else: 
            userform = Update_password(current_user)
            return render(request,'update_pass.html',{'userform':userform})
    else:
        messages.success(request,"user needs to registered first")
        return redirect('home')
    



    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user,created = ShippingAddress.objects.get_or_create(user=request.user,defaults={
                        'shipping_fullname':'',
                         'shipping_Address1' :'',
                         'shipping_email':'',
                         'shipping_zipcode':'',
                         'shipping_state':'',
        })
        cu = User.objects.get(id=request.user.id)
        userform = Update_info(request.POST or None,instance=current_user)
        
        shippingform = shipping_form(request.POST or None,instance=shipping_user)
        
        if userform.is_valid() or shippingform.is_valid():
             userform.save()
             shippingform.save()
             messages.success(request,f'{cu.first_name}\'s personal info has been updated ')
             return redirect('home')
        return render(request,'update_info.html',{'userform':userform,'shippingform':shippingform})
    else :
        messages.success(request,"user needs to login first")
        return redirect('home')


def search(request):
    if request.method == "POST":
         searched = request.POST['search']
         print(searched)
         prods = Product.objects.filter(name__icontains=searched)
         return render(request,"search.html",{'prods':prods})
    else :
     return render(request,"search.html",{})
    

def orders_invoices(request):
   return render(request,'orders_invoices.html',{})


def without_login_update_password(request,email):
        current_user = User.objects.get(email=email)
        ema = email
        userform = Update_password(current_user,request.POST)
        if userform.is_valid():
              userform.save()
              login(request,current_user)
              messages.success(request,f'{current_user.first_name}\'s password has been updated ' )
              return redirect('home')
        else:
              messages.success(request,"error in changing password" )
        
        return render(request,'change_password.html',{'userform':userform,'email':email})
   
        







def forgot_password(request):
    if request.method == "POST":
       email = request.POST.get("ema")
       verified_user = User.objects.get(email=email)
       if verified_user:
           subject = 'change password'
           rec_email = verified_user.email 
           link = 'http://localhost:8000/without_login_update_password/'+rec_email+'/'
           text_content = f"Hello,\n\nPlease click the link below to change the password:\n{link}\n\nThank you!"
           html_content = f"""
            <p>Hello,</p>
            <p>Please click the link below to visit the page:</p>
            <a href="{link}">Click Here</a>
            <p>Thank you!</p>
           """
           email_2 = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [rec_email])
           email_2.attach_alternative(html_content, "text/html")
           email_2.send()
           messages.success(request,"check your email")
    return render(request,"forgot_password.html",{})

           