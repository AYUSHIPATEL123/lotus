from django.contrib import admin
from .models import Order,OrderProduct,Payment
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','fullname','email','phone_number','city','country','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','fullname','email','phone_number']
    list_per_page=16
    inlines=[OrderProductInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
