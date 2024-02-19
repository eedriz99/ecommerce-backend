from django.db import models
from order.models import Order
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

PAYMENT_STATUS_CHOICES = {
    "INIT": 'Initiated',
    "REVW": 'Reviewed',
    "APRV": 'Approved',
    "FAIL": 'Failed'
}


class Card(models.Model):
    name = models.CharField(max_length=60)
    number = models.CharField(max_length=4)
    cvv = models.PositiveIntegerField()
    expiry_date = models.CharField(max_length=5)   # MM/YY


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)  # Payment ID
    timestamp = models.DateTimeField(
        auto_now_add=True)  # Payment timestamp
    payer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)  # User who is initiating the payment
    # Order payment is linked to
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2)  # Amount to be paid
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=4, choices=PAYMENT_STATUS_CHOICES, default="INIT", blank=True)  # status of the order, if it is processed, etc.

    def __str__(self):
        return f"{self.id}-{self.payer}-{self.timestamp}-{self.order}"
