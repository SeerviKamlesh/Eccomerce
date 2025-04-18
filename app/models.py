from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

STATE_CHOICES=(
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Rajasthan','Rajasthan'),
    ('Bengalore','Bangalore'),
    ('Andhra pradesh','Andhra pradesh'),
    ('Tamilnadu','Tamilnadu')
)
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user') 
    Product=models. ForeignKey(Product,on_delete=models.CASCADE,related_name='user')  
    quantity=models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.Product.price
    
    def __str__(self):
        return self.Product.name
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('on the way','on the way'),
    ('Deliverd','Deliverd'),
    ('cancel','cancel'),
    ('pending','pending')
)



class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    orderstatus=models.CharField(choices=STATUS_CHOICES,max_length=50,default='pending')
    order_date=models.DateField(auto_now_add=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)       