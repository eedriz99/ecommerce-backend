from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentsListSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)
