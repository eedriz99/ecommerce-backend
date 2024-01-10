from rest_framework import serializers
from .models import Order, OrderItem, Review


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data['buyer'] = self.context['buyer']
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class CartItemSerializer(serializers.Serializer):
    productID = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderRequestSerializer(serializers.Serializer):
    cartItems = CartItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
