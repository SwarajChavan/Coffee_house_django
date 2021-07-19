from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Payment)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'ordered_date', 'ordered')

    def username(self, obj):
        return obj.ordered_by.username
    def email(self, obj):
        return obj.ordered_by.email

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('username', 'transaction_id', 'productinfo', 'amount',  'status')
    def username(self, obj):
        return obj.user.username