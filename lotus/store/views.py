from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category 
from carts.models import Cartitem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create youcr views here.

def store(request,category_slug=None):
    categories=None
    products=None
    product_count=None
    if category_slug != None:
        categories=get_object_or_404(Category,slug=category_slug);
        products = Product.objects.filter(is_available=True,category=categories)
        category= Category.objects.get(slug=category_slug);
        paginator=Paginator(products,8)
        page=request.GET.get('page')
        pageed_products=paginator.get_page(page)
        product_count=products.count()
    else:    
        products=Product.objects.all().filter(is_available=True)
        category= "All Products"
        paginator=Paginator(products,8)
        page=request.GET.get('page')
        pageed_products=paginator.get_page(page)
        product_count=products.count()
    context={
        'products': pageed_products,
        'product_count':product_count,
        'category':category,
    }
    return render(request,'store/store.html',context)

def product_datails(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug);
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        e;
    context = {
        'single_product' : single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_details.html',context)