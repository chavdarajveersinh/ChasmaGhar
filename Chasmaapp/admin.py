from django.contrib import admin
from .models import ContactMessage, Product, Order, UserAccount

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')

@admin.register(UserAccount)   # 👈 new
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'side_img')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'email', 'product', 'payment', 'order_date')
    search_fields = ('customer_name', 'email', 'product__name')
    list_filter = ('payment', 'order_date')
