from django.db import models
from account.models import Account
from store.models import Product
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    payment_id = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    phone_number=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    country=models.CharField(max_length=50)    
    state=models.CharField(max_length=50)    
    city=models.CharField(max_length=50)
    order_totle=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=50,choices=STATUS,default='New')
    ip=models.CharField(max_length=50,null=False,blank=False)
    is_ordered = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)   

    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.first_name
    
class OrderProduct(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product.product_name)
    
    def prod_total(self):
        return int(self.product_price*self.quantity);