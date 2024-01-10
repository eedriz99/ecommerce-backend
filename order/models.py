from django.db import models
from django.conf import settings
import uuid

from product.models import Product
# from userProfile.models import userProfile

# Create your models here.

STATUS_CHOICES = {
    "SUB": "Submitted",
    "INP": "In Progress",
    "PRO": "Processed",
    "FLD": "Failed"
}


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)  # Order ID
    timestamp = models.DateTimeField(
        auto_now_add=True)  # Date of order creation
    # User who is initiating the order
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # status of the order, if it is processed, etc.
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default="SUB", blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.id}-{self.buyer}-{self.timestamp}"


class OrderItem(models.Model):
    """A single item in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order}-{self.product}-{self.quantity}"


class Review(models.Model):
    product = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    # buyer = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    datetime = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product}-{Order.buyer}"
