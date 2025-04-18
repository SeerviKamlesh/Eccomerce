from django.shortcuts import render,redirect,get_object_or_404
from .forms import Registration,Customerform
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
from .models import Product, Category ,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import razorpay 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings  

@login_required(login_url='/login/')
def product_list(request, id=None):
    object = Cart.objects.filter(user=request.user).count()

    categories = Category.objects.all()
    if id:
        products = Product.objects.filter(category_id=id)
    else:
        products = Product.objects.all()
    
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'object':object
    })

def product_details(request,pk):
    product=Product.objects.get(pk=pk)
    object = Cart.objects.filter(user=request.user).count()

    return render(request,'product_details.html',locals())

class Customerregistration(View):
    def get(self,request):
        form=Registration()
        return render(request,'registration.html',locals())
    def post(self,request):
        form=Registration(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                return messages.error(request,'user alredy exist')
            form.save()
            messages.success(request,'congratulations user register successfully')
            return redirect('/home/')
        else:
            messages.error(request, 'Error in input fields')
            return render(request, 'registration.html', {'form': form})  # <
        

def userlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password') 
        
        if User.objects.filter(username=username).exists():

            user=authenticate(request,username=username,password=password) 
            if user!= None:
                login(request,user)
                return redirect('/home/')    
            else:
                messages.error(request,'invalid username or password')
                return redirect('/login/')
        else:
             messages.error(request,'user doesnot exist')

    else:
        return render(request,'userlogin.html')         
    
class profile(View):
    def get(self,request):
        form=Customerform()
        object = Cart.objects.filter(user=request.user).count()

        return render(request,'Add_Address.html',locals())
    def post(self,request):
        form=Customerform(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile'] 
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            profile=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            profile.save()
            messages.success(request,'profile created successfully')
        else:
            messages.warning(request,'invalid data')
        return redirect('/profile/')
    
def address(request):
    object = Cart.objects.filter(user=request.user).count()
    address=Customer.objects.filter(user=request.user)
    return render(request,'address.html',{'address':address,'object':object})


def updateAddress(request,id):
    object = Cart.objects.filter(user=request.user).count()

    address=Customer.objects.get(id=id)
    form=Customerform(instance=address)
    if request.method =='POST':
       form=Customerform(request.POST)
       if form.is_valid():
            address=Customer.objects.get(id=id)
            address.name=form.cleaned_data['name']
            address.locality=form.cleaned_data['locality']
            address.city=form.cleaned_data['city']
            address.mobile=form.cleaned_data['mobile'] 
            address.state=form.cleaned_data['state']
            address.zipcode=form.cleaned_data['zipcode']
            address.save()
            messages.success(request,'address updated successfully')
            return redirect('/address/')
    return render(request,'updateaddress.html',locals())


def add_to_cart(request,id):
    user=request.user
    product=Product.objects.get(id=id)
    if Cart.objects.filter(user=user,Product=product).exists():
        messages.info(request,'alredy added to cart')
        return redirect('/show_cart/')
    Cart.objects.create(user=user,Product=product)
    return redirect('/show_cart/')

def show_cart(request):
    object = Cart.objects.filter(user=request.user).count()

    user=request.user
    products=Cart.objects.filter(user=user)
    amount=0
    for p in products:
        value=p.quantity*p.Product.price
        amount+=value
    totalamount=amount+40    
    return render(request,'showcart.html',locals())    

def plus_cart(request):
    if request.method=='GET':
        proid=request.GET.get('prod_id')
        c=Cart.objects.get(Q(Product=proid)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        product=Cart.objects.filter(user=user)
        amount=0
        for p in product:
            value=p.quantity*p.Product.price
            amount+=value
        totalamount=amount+40    
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method=='GET':
        proid=request.GET.get('prod_id')
        c=Cart.objects.get(Q(Product=proid)& Q(user=request.user))
        if c.quantity>0:
            c.quantity-=1
            c.save()
        user=request.user
        product=Cart.objects.filter(user=user)
        amount=0
        for p in product:
            value=p.quantity*p.Product.price
            amount+=value
        totalamount=amount+40    
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove(request):
    if request.method=='GET':
        proid=request.GET.get('prod_id')
        c=Cart.objects.get(Q(Product=proid)& Q(user=request.user))
        c.delete()
        user=request.user
        product=Cart.objects.filter(user=user)
        amount=0
        for p in product:
            value=p.quantity*p.Product.price
            amount+=value
        totalamount=amount+40    
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)    

 
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    amount=0
    cart_items=Cart.objects.filter(user=user)
    for item in cart_items:
        value=item.Product.price*item.quantity
        amount+=value
    totalamount=amount+40   
    razorpayamount=int(totalamount*100) 
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data= {
    "amount": razorpayamount,
    "currency": "INR",
    "payment_capture":"1"}
    payment_response=client.order.create(data=data)
    order_id=payment_response['id']
    order_satus=payment_response['status']
    if order_satus=='created':
        payment=Payment(user=user,amount=razorpayamount,razorpay_order_id=order_id,razorpay_payment_status=order_satus)
        payment.save()
    print(payment_response)
    return render(request,'checkout.html',locals())


# def checkoutrender(request):
#     user=request.user
#     add=Customer.objects.filter(user=user)
#     amount=0
#     cart_items=Cart.objects.filter(user=user)
#     for item in cart_items:
#         value=item.Product.price*item.quantity
#         amount+=value
#     totalamount=amount+40  
#     return render(request,'checkout.html',locals()) 

def paymentdone(request):
    addressid=request.GET.get('custid')
    if not addressid:
        messages.error(request, "Please select an address before proceeding to payment.")
        return redirect('checkout')
    address=Customer.objects.get(id=int(addressid))
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    userid=request.GET.get('userid')
    user=User.objects.get(id=int(userid))
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.razorpay_payment_id=payment_id
    payment.paid=True
    payment.save()
    cart_items=Cart.objects.filter(user=user)
    for c in cart_items:
        OrderPlaced.objects.create(user=user,customer=address,product=c.Product,quantity=c.quantity,payment=payment)
        c.delete()
    # the reason iam using login here is that when razorpay excutes it will logout the user and due to this iam using login to redirect to home 
    # login(request, user) after the Razorpay callback makes sense to restore the session if the user was logged out due to the external callback.
    login(request,user)    
    # email logic
    try:
        context = {
            'user': user,
            'order_id': order_id,
            'payment_id': payment_id,
            'amount': payment.amount,  # Assuming amount is stored in payment model
            'address': address,
        }
        
        html_content = render_to_string('order_confirmation.html', context)
        text_content = strip_tags(html_content)
        from_email = 'rajsirvi123456@gmail.com'
        recipient_email = user.email
        
        email = EmailMultiAlternatives(
            'Order Confirmation',
            text_content,
            from_email,
            [recipient_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print("EMAIL ERROR:", e)
    return redirect('/my-orders/')    





# testing view by usding json
from django.views.decorators.csrf import csrf_exempt
@ csrf_exempt
def checkout1(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    amount=0
    cart_items=Cart.objects.filter(user=user)
    for item in cart_items:
        value=item.Product.price*item.quantity
        amount+=value
    totalamount=amount+40   
    razorpayamount=int(totalamount*100) 
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data= {
    "amount": razorpayamount,
    "currency": "INR",
    "payment_capture":"1"}
    payment_response=client.order.create(data=data)
    order_id=payment_response['id']
    order_satus=payment_response['status']
    if order_satus=='created':
        payment=Payment(user=user,amount=razorpayamount,razorpay_order_id=order_id,razorpay_payment_status=order_satus)
        payment.save()
    print(payment_response)

    return JsonResponse({
        "order_id":payment_response['id'],
        "razorpay_key_id":settings.RAZOR_KEY_ID,
        "razorpay_key_secret":settings.RAZOR_KEY_SECRET,
        "amount":razorpayamount,
        "razorpay_callback_url":"http://localhost:8000/paymentdone/"
    })   

def logout_user(requset):
    logout(requset)
    return redirect('/login/')

@login_required
def my_orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        return redirect('/wishlist_page/')
    messages.info(request, "This item is already in your wishlist.")
    return redirect('product_details', pk=product.id)  

@login_required
def remove_from_wishlist(request, product_id):
    wishlist_item = Wishlist.objects.filter(user=request.user, product__id=product_id).first()
    if wishlist_item:
        wishlist_item.delete()
    else:
        messages.info(request, "Item not found in wishlist.")
    return redirect('wishlist_page')

@login_required
def profile1(request):
    user=request.user
    orders=OrderPlaced.objects.filter(user=user)
    print(orders)
    return render(request,'profile.html',{'orders': orders})
