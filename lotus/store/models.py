from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    discription=models.TextField(max_length=500)
    price=models.IntegerField()
    stock=models.IntegerField()
    image=models.ImageField(upload_to='photos/products')
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name;
    
    def get_url(self):
        return reverse("datails_by_product",args=[self.category.slug,self.slug]);