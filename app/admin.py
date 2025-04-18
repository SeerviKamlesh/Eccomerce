from django.contrib import admin

# Register your models here.
from .models import Product, Category,Customer,Cart,Payment,OrderPlaced,Wishlist

@admin.register(Product)
class productmodeladmin(admin.ModelAdmin):
    list_display=['id','name','category','price','stock','created_at']
admin.site.register(Category)

@admin.register(Customer)
class CustomermodelAdmin(admin.ModelAdmin):
    list_display=['user','name','locality','city','zipcode','state','mobile']

@admin.register(Cart)
class  CartmodelAdmin(admin.ModelAdmin):
    list_display=['id','user','Product','quantity']   

@admin.register(Payment)
class PaymentmodelAdmin(admin.ModelAdmin):
    list_display=['user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']   

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['user','customer','product','quantity','orderstatus','order_date','payment']    


admin.site.register(Wishlist)    