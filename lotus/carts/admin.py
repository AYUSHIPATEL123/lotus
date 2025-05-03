from django.contrib import admin
from .models import Cart,Cartitem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')

admin.site.register(Cart,CartAdmin)


class CartItemsAdmin(admin.ModelAdmin):
    list_display=('product','cart','is_active','quintity')

admin.site.register(Cartitem,CartItemsAdmin)
