from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from payment.models import Order,OrderItem
from .utils import generate_invoice
from .models import user_inv,wishlist,blog
from io import BytesIO
from store.models import Product
from django.contrib import messages
from .forms import Reviewform

# Create your views here.
@receiver(post_save,sender=OrderItem)
def creat_invoice(sender,instance,created,**kwargs):
   if created:
      
      order = instance.order  
        
        
      order_items = order.orderitem_set.all()
      
      invoice = user_inv.objects.create(invoice_number=f'{instance.id}',order=order,user=instance.user)
      invoice.items.set(order_items) 
      buffer = BytesIO()
      generate_invoice(invoice, buffer)  
      buffer.seek(0) 
      file_name = f'invoice_{invoice.invoice_number}.pdf'
      invoice.pdf_file.save(file_name, ContentFile(buffer.getvalue()), save=True)
      buffer.close()


def invoice_view(request,invoice_id):
   invoice = get_object_or_404(user_inv,id=invoice_id)
   buffer = generate_invoice(invoice)
   response = HttpResponse(buffer,content_type="application/pdf")
   response['Content-Disposition'] = f'inline; filename="invoice_{invoice.invoice_number}.pdf"'
   return response

 
    
def invoice_detail(request):
   invoice = user_inv.objects.filter(user=request.user.id)
   print(invoice)
   return render(request,'inv_detail.html',{'invoice':invoice})

def add_to_wishlist(request):
    if request.user.is_authenticated:
      print("enetered")
      product_id = request.POST.get("product")
      product = get_object_or_404(Product,id=product_id)
      print(product_id)
      if wishlist.objects.filter(user=request.user,product=product).exists():
          return messages.success(request,"Product already exists in your wishlist")
    
      wishlist.objects.create(user=request.user,product=product)
      messages.success(request,"Added to wishlist")
      return redirect('home')
    else:
       return messages.success("please,signup first to add product on wishlist")
    
       
def remove_from_wishlist(request):
    if request.user.is_authenticated:
       product_id = request.POST.get("product")
       prod = get_object_or_404(wishlist,user=request.user,product=product_id)
       prod.delete()
       messages.success(request,"Product removed from wishlist")
       return redirect('view_list')
    else:
       return messages.success("wait for some time,inconvenience from our side")
       
       
    

def view_list(request):
   if request.user.is_authenticated:
      wish = wishlist.objects.filter(user=request.user)
      
      return render(request,"view_list.html",{"wish":wish})



def create_blog(request):
    if request.user.is_authenticated:
     if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        img = request.FILES.get('image')
        bl = blog(title=title,content=content,img=img,user=request.user)
        bl.save()
        return redirect('view_blogs')
     else:
        return render(request,'blog.html',{})
     
    

def view_blogs(request):
   blogs = blog.objects.all()
   return render(request,"view_blogs.html",{'blogs':blogs})
       

def detailed_blog(request,pk):
   bl = blog.objects.get(id=pk)
   return render(request,"detailed_blog.html",{'bl':bl})

def list_invoices(request):
   invoices = user_inv.objects.all().order_by('created_at')
   return render(request,'list_invoices.html',{'invoices':invoices})