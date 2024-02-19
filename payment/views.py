from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from .models import Payment
from  .serializers import PaymentSerializer, PaymentsListSerializer
from order.models import Order

import stripe

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
# Create your views here.

stripe.api_key = "sk_test_51OhqmwIWOqV6bPeLziw0NnaXrrugsh6VXaKDaMjwIgL088XQo6DI5ukbxvri3wTk0mqK0PsuMIJmTZaQL4xQA5iz00bwGzfWie"

@api_view(['GET','POST'])
def initiate_payment(request):
    
