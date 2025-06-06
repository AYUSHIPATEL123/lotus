from datetime import timezone
from django.db import models
from store.models import Product
from account.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id=models.CharField(max_length=50,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class Cartitem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)  
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quintity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quintity
                                                    
    def __str__(self):
        return self.product.product_name
