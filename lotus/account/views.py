from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from lotus.settings import EMAIL_HOST_USER
from carts.models import Cart,Cartitem
from carts.views import _cart_id
# Create your views here.

def registration(request):
    if request.method =='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
        
            user = Account.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            user.phone_number = phone_number
            user.save()
            # activation process
            current_site=get_current_site(request)
            mail_subject="please activate your account"
            message = render_to_string('account/account_varifucation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            # from_email='patelayu153@gmail.com'
            # send_email_massage= EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
            send_email_massage = EmailMessage(
                                                subject=mail_subject,
                                                body=message,
                                                from_email=EMAIL_HOST_USER,
                                                to=[to_email]
                                            )
            user.is_active = False
            send_email_massage.fail_silently = False
            send_email_massage.send()
            messages.success(request,"we send the activation link to your email....")
            return redirect('register')
    else:
        form=RegistrationForm()

    context={
        'form':form,
    }
    return render(request,'account/register.html',context)


def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                print("you are in try block")
                cart=Cart.objects.get(cart_id=_cart_id(request))
                print(cart)
                is_cart_items_exist=Cartitem.objects.filter(is_active=True,cart=cart).exists()
                print(is_cart_items_exist)
                if is_cart_items_exist:
                    cartitem=Cartitem.objects.filter(cart=cart)
                    print(cartitem)
                    for item in cartitem:
                        item.user=user
                        item.save()

            except Cart.DoesNotExist:
                print("you are in except block")
                pass    
            auth.login(request,user)
            # messages.success(request,"logged in successful...")
            return redirect('home')
        else:
            messages.error(request,"invalid caradencials...")
            return redirect('login')
    return render(request,'account/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"logged out successfuly..")
    return redirect('login')

@login_required(login_url='login')
def update(request):
    if request.method =='POST':
        first_name=request.POST.get('f_name')
        last_name=request.POST.get('l_name')
        email=request.POST.get('email')
        phone_number=request.POST.get('ph_no')
        
        try:
            user=Account.objects.get(id=request.user.id)
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.phone_number=phone_number
            user.save()
            messages.success(request,"your profile has been updated")
            return redirect('profile', pk=user.pk)
        except:    
            messages.error(request,'fail to update profile')
    return render(request,'account/profile.html')

import logging

logger = logging.getLogger(__name__)
def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError) as e:
        logger.error(f"Error decoding uidb64 or fetching user: {str(e)}")
        user = None
    except Account.DoesNotExist:
        logger.error(f"User with UID {uidb64} does not exist.")
        user = None


    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"congratulations,your account is activated")
        return redirect('login')
    else:
        messages.error(request,"this link is expired...")
        return redirect('register')
            

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)

            current_site=get_current_site(request)
            mail_subject="reset your password"
            message = render_to_string('account/resetpassword_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            # from_email='patelayu153@gmail.com'
            # send_email_massage= EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
            send_email_massage = EmailMessage(
                                                subject=mail_subject,
                                                body=message,
                                                from_email=EMAIL_HOST_USER,
                                                to=[to_email]
                                            )
            user.is_active = False
            send_email_massage.fail_silently = False
            send_email_massage.send()
            messages.success(request,"we send the reset password link to your email....")
            return redirect('login')
        else:
            messages.error(request,"account does not exist")
            return redirect('forgot')
    return render(request,'account/forgotpassword.html') 

def resetPassword_validation(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError) as e:
        logger.error(f"Error decoding uidb64 or fetching user: {str(e)}")
        user = None
    except Account.DoesNotExist:
        logger.error(f"User with UID {uidb64} does not exist.")
        user = None


    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"please reset the password...")
        return redirect('reset')
    else:
        messages.error(request,"this link is expired...")
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password=request.POST['password']    
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"password is reseted sucssessfully")
            return redirect('login')
        else:
            messages.error(request,"password does't matched")
            return redirect('reset') 
    else:           
        return render(request,'account/resetpassword.html')
    
login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password=request.POST['c_pass']    
        new_password=request.POST['new_pass']    
        confirm_password=request.POST['con_pass']

        user=Account.objects.get(username=request.user.username)

        if new_password==confirm_password:
            success=user.check_password(current_password);
            if success:
                user.set_password(new_password);
                user.save()
                messages.success(request,"your password has been changed.")
                return redirect('change_pass')
            else:
                messages.error(request,"please enter the right old password.")
                return redirect('change_pass')
        else:
            messages.error(request,"passwords does not matched.")
    return render(request,"account/change_password.html")        
