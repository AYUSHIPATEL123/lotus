
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import store,product_datails
urlpatterns = [
    path('',store,name='store'),
    path('<slug:category_slug>/',store,name="product_by_category"),
    path('<slug:category_slug>/<slug:product_slug>/',product_datails,name="datails_by_product"),
] 
