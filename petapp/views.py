from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib import messages
import datetime
from django.contrib.auth import authenticate,login,logout
from .models import Cart,Orders,Customer_details
from django.db.models import Q
from .forms import petform,RegisterForm,UserAuthentication,UserauthenticationForm,Customer_detailsform

from django.contrib.auth.decorators import login_required
 
 
from django.conf import settings
import uuid

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse


#================ Forgot Password ======================
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse






from django.views import View

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import customerserializer


def register(request):
    if request.method=='POST':
        fm=RegisterForm(request.POST)
        print(fm)
        uname=request.POST['username']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        context={}
        if uname=="" or pass1=="" or pass2=="":
            context['errmsg']="Field cannot be empty"
            return render(request,'register1.html',context)
        elif pass1 !=pass2:
            context['errmsg']="Password and Confirm password must be same "
        if fm.is_valid():
            fm.save()
            
            return redirect('home')

    else:
        fm=RegisterForm()
        return render(request,'register1.html',{'forms':fm})


 

  

import datetime
def user_login(request):
    if request.method=="POST":
        uname=request.POST['username']
        upass=request.POST['password']
        user=authenticate(request,username=uname,password=upass)
        if user is not None:
            login(request,user)
      
            response=redirect('home')
            request.session['username']=uname
            response.set_cookie('Username',uname)
            response.set_cookie('time',datetime.datetime.now())
            return response         
        else:
            
            fm=UserAuthentication()

            return render(request,'userlogin.html',{'forms':fm,'msg':'Wrong Credentials!!'})
    else:
        fm=UserAuthentication()

        return render(request,'userlogin.html',{'forms':fm})




def signout(request):
    logout(request)
   
    return redirect('home')





  
            
  
   






from .models import Breed,Pet
# Create your views here.
def show(request):
    breed=Breed.objects.all()
    pet=Pet.objects.all()
    context={}
    context['pet']=pet
    
    
    context['breed']=breed
    return render(request,'home.html',context)
     
 
def addprod(request,id):
    pet=Pet.objects.filter(id=id)
    context={'pet':pet}
    data=Pet
    return render(request,"product.html",context) 
 








from .forms import petform

def addpet(request):
    if request.method=="POST":
        fm=petform(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            return HttpResponse("successfully saved")
    else:
        fm=petform()
        return render(request,'addpet.html',{'forms':fm})

from django.contrib.auth.models import User
from django.db.models import Q

@login_required(login_url='user_login')
def addtocart(request,pid):
        # userid=request.user.id   
        # # print(userid)
        # # print(pid)
        # u=User.objects.filter(id=userid)  #4
        # #print(u[0])
        # p=Pet.objects.filter(id=pid)
        # #print(p[0])    #5
        
        # c=Cart.objects.create(uid=u[0],pid=p[0])
        # c.save()
        # return HttpResponse("Product added to cart")
    
    if request.user.is_authenticated:
        userid=request.user.id   #4
        print(userid)
        print(pid)
        u=User.objects.filter(id=userid)  #4
        #print(u[0])
        p=Pet.objects.filter(id=pid)
        #print(p[0])    #5
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)    #queryset[1 object]
        print(c)
        n=len(c)
        context={}
        context={'pet':p}
        if n == 1:
            context['msg']="Product already Exists in Cart !!"
            return render(request,'product.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="product Added Successfully to cart !!"
            return render(request,'product.html',context)
            #return HttpResponse("Product added in the cart")
   
    

  
def viewcart(request):
    cart_data=Cart.objects.filter(uid=request.user.id)
    
    total=0
    for x in cart_data:
        total=total+x.pid.price*x.qty #price is calculated by pid which is in cart model 
                                       #and pid reated to price
       
    context={}
    context['data']=cart_data
    context['total']=total
    return render(request,'cart.html',context)

 


def updateqty(request,qv,cid):
     c=Cart.objects.filter(id=cid)
     if qv=='1':
         t=c[0].qty+1
         c.update(qty=t)

     return redirect('/viewcart') 

















def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        pass
    return redirect('/viewcart') 




def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

 

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    total=0    
    for x in c:
        print(x.pid)
        print(x.uid)
        print(x.qty)
        total_data=total+x.pid.price*x.qty
        print(total_data)
        o=Orders.objects.create(pet=x.pid,customer=x.uid,quantity=x.qty,total_price=total_data)
        o.save()
        x.delete()
    
    orders=Orders.objects.filter(customer=request.user.id)
    print(orders)
    total=0
    for i in orders:
        total=total+i.total_price
    print(total)
    context={}
    context['data']=orders
    context['total']=total
    return render(request,'placeorder.html',context)




def checkoutnew(request):
    userid=request.user
    print(userid)
    cart_items = Orders.objects.filter(customer=userid)
       # cart_items will fetch product of current user, and 
       # show product available in the cart of the current user.
    print(cart_items)
    total =0
    delivery_charge =500
    total=0
    for x in cart_items:
        total=total+x.total_price*x.quantity
    final_price= delivery_charge + total
    print("final_price",final_price)
    
    # cust_details=Customer_details.objects.filter(user=request.user)
  
    # for i in cust_details:
    #     contact_address=i.address
    # print(contact_address)

    cust_deatils=Customer_details.objects.filter(user=request.user)

  
  #================= Paypal Code =====================
   
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
        'amount': final_price,    #: The amount of money to be charged for the transaction. 
        'item_name': 'Pet',       # Describes the item being purchased.
        'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
        'return_url': f"http://{host}{reverse('paymentsuccess')}",     #The URL where the customer will be redirected after a successful payment. 
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

  #================= Paypal Code  End =====================

    
    
    
    
   
         
   
    return render(request, 'checkout.html', {'cust_deatils':cust_deatils,'cart_items': cart_items,
            'total':total,'final_price':final_price,'paypal':paypal_payment})


def customer_address(request):
     if request.method=="POST":
        fm=Customer_detailsform(request.POST)
        name=request.POST['name']
            
        city =request.POST['city']
        state = request.POST['state']
        pincode=request.POST['pincode']
        context={}
        if name=="" or city=="" or state=="":
            context['errmsg']="Field cannot be empty"
            return render(request,'address.html',context)
         
        if fm.is_valid():
            data=fm.save(commit=False)
            data.user=request.user
            data.save()
            
            
            return redirect('home')

     else:    
        mf =Customer_detailsform()
        return render(request,'address.html',{'form':mf})


def paymentsuccessful(request):
    print('payment sucess')    
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    total=0    
    for x in c:
        print(x.pid)
        print(x.uid)
        print(x.qty)
        total_data=total+x.pid.price*x.qty
        print(total_data)
        o=Orders.objects.create(pet=x.pid,customer=x.uid,quantity=x.qty,total_price=total_data)
        o.save()
        x.delete()
    
    orders=Orders.objects.filter(customer=request.user.id)
    print(orders)
    total=0
    for i in orders:
        total=total+i.total_price
    print(total)
    context={}
    context['data']=orders
    context['total']=total
    
    return render(request,'paymentsuccessful.html',context)

def paymentfailed(request):
    return render(request,'paymentfailed.html')
def checkout(request):
    return render(request,'checkout.html')






def breed_view(request,id):
    breed=Breed.objects.all()
    pet=Pet.objects.filter(breed=id)

    context={'breed':breed,'pet':pet}
    return render(request,'home.html',context)

def showpet(request,id):
    pet=Pet.objects.filter(id=id) 
    return render(request,'products.html',{'pet':pet})



def searchproduct(request):
    if request.method=="POST":
        data=request.POST['search']
        print(data)
      
        searchdata=Pet.objects.filter(petname__icontains=data)
        print(searchdata)
        return render(request,'search.html',{'searchdata':searchdata})
    else:
        return redirect('home')
    
 
def sort(request,sv):
    
      if sv=='0':
          col='price'     #asc
      else:
          col='-price'    #desc
      pet=Pet.objects.all().order_by(col)   #select * from product where is_active=true order by asc/desc
      context={}
      context['pet'] =pet
      return render(request,'home.html',context)


from .models import Pet
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    print(min)
    print(max)
    q1=Q(price__lte=max) #5000
    q2=Q(price__gte=min) #1000
    c=Pet.objects.filter(q1 & q2)# select * from pet where price>1000 and price<5000;
    context={}
    context['pet']=c
    return render(request,'home.html',context)













from django.contrib.auth.forms import UserCreationForm

 



def petview(request):
    if request.method=="POST":
        fm=petform(request.POST)
        if fm.is_valid():

            return HttpResponse("DATA IS SAVED")
    else:

        fm=petform()
        return render(request,"petform.html",{'forms':fm})





from django.contrib.auth import authenticate,login


def logindetails(request):
    if request.method=="POST":
        uname=request.post["username"]
        upass=request.post["password"]
        user=authenticate(request,username=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('home')
    else:
        fm=UserauthenticationForm()
        return render(request,"login_details.html",{'forms':fm})
def order(request):
    ord=Orders.objects.filter(customer=request.user)
    return render(request,'order.html',{'ord':ord})



# def set_cookie(request):
#     response=HttpResponse("Cookie set")
#     response.set_cookie('username','Priya')
#     return response
# def get_cookie(request):
#     username=request.COOKIES.get('username')
#     print(username)
#     return render(request,'getcookie.html',{'username':username})

def forgot_password(request):          

    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the given link to reset your password: {reset_url}',
                'techpy119@gmail.com',  # Use a verified email address
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'please enter valid email address')
    return render(request, 'forgot_password.html')
 
def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        print(password)
        password2 = request.POST['password2']
        print(password2)
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'reset_password.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')




class crud_api(APIView):
    def post(self,request):
        data=request.data
        #print(data)
        serializer=customerserializer(data=data)
        #print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Successfully data inserted'},status=status.HTTP_200_OK)
        return Response({'msg':'Couldnt insert data'},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        id=request.data.get('id',None)
        if id:
            try:
                student_data=Customer_details.objects.get(id=id)
                serializer=customerserializer(student_data)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return Response({'error':"Data does not exists"},status=status.HTTP_404_NOT_FOUND)  
        else:
            student_data=Customer_details.objects.all()
            serializer=customerserializer(student_data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)











 







