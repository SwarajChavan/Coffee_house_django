from django.db import models
from Home.models import  *
from django.conf import settings
from django.core import  validators
from django.core.validators import *
from django_countries.fields import CountryField
from Users.models import NewUser
# Create your models here.


class Orders(models.Model):
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    checkout_address = models.CharField(max_length=300,  blank=True)

    def __str__(self):
        return self.ordered_by.username

    def get_total_price(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    class Meta:
        db_table = "orders"

class Payment(models.Model):
    class Status_choices(models.TextChoices):
        Pending = 'Pending'
        Successful = 'Successful'
        Failed = 'Failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=False)
    productinfo= models.CharField(max_length=100, null=True)
    hash = models.CharField(max_length=300)
    status = models.CharField(choices=Status_choices.choices,max_length=10, default='Pending', null=False)
    timestamp = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'payment'
