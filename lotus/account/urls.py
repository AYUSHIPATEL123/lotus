from django.contrib import admin
from django.urls import path,include
from .views import registration,login,logout,activate,forgotPassword,resetPassword_validation,resetPassword,update,change_password
urlpatterns = [
    path('register/',registration,name='register'),    
    path('login/',login,name='login'),    
    path('logout/',logout,name='logout'),    
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('forgot/',forgotPassword,name='forgot'),    
    path('resetpassword/',resetPassword,name='reset'),    
    path('reset/<uidb64>/<token>/',resetPassword_validation,name='reset_val'),
    path('profile/',update,name='profile'),
    path('change_password/',change_password,name='change_pass'),    
] 
