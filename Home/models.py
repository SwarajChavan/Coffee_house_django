from django.db import models
from django.shortcuts import reverse
from django.core.validators import *
from django.conf import settings

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    beverage = models.BooleanField(default=False)
    snack = models.BooleanField(default=False)
    discontinued=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk":self.pk
        })

    def get_remove_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk" : self.pk
        })
    class Meta:
        db_table = "items"


# Order item stores the product quantity and total price that user wants to order
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(10)], default=1 )

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return int(self.quantity)*int(self.item.price)

    class Meta:
        db_table = "order_items"
