from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from carts.models import Cartitem
from .forms import OrderForm
from .models import Order,OrderProduct,Payment
from store.models import Product
import datetime
import json
from lotus.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def payment(request):
    body=json.loads(request.body)
    print(body)
    order=Order.objects.get(user=request.user,order_number=body['order_id'],is_ordered=False)
    payment=Payment(
        user=request.user,
        payment_id=body['trans_id'],
        status=body['status'],
        payment_method=body['payment_method'],
        amount_paid=order.order_totle
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()

    cartitems=Cartitem.objects.filter(user=request.user)
    
    for cart_item in cartitems:
        orderproduct=OrderProduct()
        orderproduct.user=request.user
        orderproduct.payment=payment
        orderproduct.order=order
        orderproduct.product=cart_item.product
        orderproduct.quantity=cart_item.quintity
        orderproduct.product_price=cart_item.product.price
        orderproduct.is_ordered=True
        orderproduct.save()
    # user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    # payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)
    # order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    # product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    # quantity=models.IntegerField()
    # product_price=models.FloatField()
    # is_ordered = models.BooleanField(default=False)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)
        product= Product.objects.get(id=cart_item.product.id)
        product.stock -= cart_item.quintity
        product.save()

    

    mail_subject="recived order"
    message = render_to_string('order/order_recived_email.html',{
                    'user':request.user,
                    'order':order,
                    'cartitems':cartitems,
                })
    to_email=request.user.email
                # from_email='patelayu153@gmail.com'
                # send_email_massage= EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
    send_email_massage = EmailMessage(
                                        subject=mail_subject,
                                        body=message,
                                        from_email=EMAIL_HOST_USER,
                                        to=[to_email]
                                    )
    
    send_email_massage.fail_silently = False
    send_email_massage.send()
    cartitems.delete()
    data={
        'order_id':order.order_number,
        'tran_id':payment.payment_id,
    }
    return JsonResponse(data)

   

def placeorder(request,total=0,quintity=0):
    current_user = request.user

    cart_items=Cartitem.objects.filter(user=current_user)
    count=cart_items.count()
    if count <=0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quintity)
        quintity += cart_item.quintity
    tax=(2*total)/100
    grand_total=total+tax  

    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.phone_number=form.cleaned_data['phone_number']
            data.address=form.cleaned_data['address']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.country=form.cleaned_data['country']
            data.order_totle=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number=current_date + str(data.id)
            data.order_number=order_number
            data.save()
            order=Order.objects.get(user=current_user,order_number=order_number,is_ordered=False)

            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'order/payment.html',context)
        else:
            return redirect('checkout')
    
    return render(request,'store/checkout.html')     
        
def ordercomplete(request):
    order_id=request.GET.get('order_id');
    trans_id=request.GET.get('tran_id');

    try:
        order=Order.objects.get(order_number=order_id,is_ordered=True)
        orderproducts=OrderProduct.objects.filter(order=order)
        sub_total=0
        for item in orderproducts:
            sub_total +=(item.product_price*item.quantity);
        payment=Payment.objects.get(payment_id=trans_id)
        context={
            'order':order,
            'orderproducts':orderproducts,
            'trans_id':trans_id,
            'order_id':order_id,
            'payment':payment,
            'sub_total':sub_total,
        }

        return render(request,'order/ordercomplete.html',context)
    except (Order.DoesNotExist,OrderProduct.DoesNotExist):
        return redirect('home')