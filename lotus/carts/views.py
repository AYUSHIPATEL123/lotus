from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,Cartitem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session._session_key
    if not cart:
        request.session.create()
    return cart
    
def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        if request.user.is_authenticated:
            cart_item=Cartitem.objects.get(product=product,user=request.user)
        else:
            cart_item=Cartitem.objects.get(product=product,cart=cart)    
            cart_item.user=None
        cart_item.quintity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        if request.user.is_authenticated:
            user=request.user
        else:
            user=None
        cart_item=Cartitem.objects.create(
            product=product,
            cart=cart,
            quintity = 1,
            user=user
        )   
    cart_item.save()  
    return redirect('cart')
     
def remove_cart(request,product_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id = _cart_id(request))
        cart_item = Cartitem.objects.get(product=product,cart=cart)    
    if cart_item.quintity > 1:
        cart_item.quintity -= 1
        cart_item.save()
    else:
        cart_item.delete() 
    return redirect('cart')

def remove_cart_item(request,product_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=Cartitem.objects.get(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id = _cart_id(request))
        cart_item=Cartitem.objects.get(product=product,cart=cart)    
        cart_item.user=None
    # cart_item = Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
       
def cart(request, total=0,quintity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(is_active=True,user=request.user)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(is_active=True,cart=cart)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quintity)
            quintity += cart_item.quintity
        tax=(2*total)/100
        grand_total=total+tax
    except Cart.DoesNotExist: 
           pass  

    context={
        'cart_items':cart_items,
        'quintity':quintity,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
    }       
    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0,quintity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(is_active=True,user=request.user)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(is_active=True,cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quintity)
            quintity += cart_item.quintity
        tax=(2*total)/100
        grand_total=total+tax
    except Cart.DoesNotExist: 
           pass  

    context={
        'cart_items':cart_items,
        'quintity':quintity,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
    }       
    return render(request,'store/checkout.html',context)

