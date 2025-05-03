from django.shortcuts import render
from store.models import Product
def home(request):
    products=Product.objects.all().filter(is_available=True)
    print(products)
    context={
        'products': products
    }
    return render(request,'home.html',context)
def signup(request):
    return render(request,'register.html')
def login(request):
    return render(request,'login.html')
def aboutus(request):
    return render(request,'about.html')
