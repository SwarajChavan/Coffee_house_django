from django.contrib import admin
from.models import *
# Register your models here.

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display= ('name', 'price', 'beverage', 'snack')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'item', 'quantity', 'price',  'ordered')

    def username(self, obj):
        return obj.user.username
    def email(self, obj):
        return obj.user.email
    def price(self, obj):
        return obj.quantity * obj.item.price