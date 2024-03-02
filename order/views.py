from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Serializer imports
from .serializer import OrderItemSerializer, OrderSerializer, ReviewSerializer, OrderRequestSerializer

# Model imports
from .models import Order, OrderItem, Review
from product.models import Product
from django.contrib.auth import get_user_model

# Rest framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status


User = get_user_model()

# Create your views here.


@api_view(['GET', 'POST'])
@login_required(login_url='/login/')
def orders_view(request):
    if request.method == "GET":
        querySet = Order.objects.filter(
            buyer=request.user).order_by('timestamp')
        serializer = OrderSerializer(querySet, many=True)
        return Response({"Orders": f"{serializer.data}"}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OrderRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Will only save if all transactions (processes) are successful.
                with transaction.atomic():
                    total = serializer.validated_data['total']
                    cartItems = serializer.validated_data['cartItems']
                    # Get curret User object using the user attribute returned from the request object.
                    current_user = User.objects.get(
                        email=request.user)
                    # Create an Order object with buyer being the current user and a total from the data from the frontend.
                    order = Order.objects.create(
                        buyer=current_user, total=total)
                    order_items = [OrderItem(order=order, product=Product.objects.get(
                        productID=item['productID']), quantity=item['quantity']) for item in cartItems]

                    OrderItem.objects.bulk_create(order_items)
                    return Response({'message': f'Order of {len(order_items)} items created successfully', 'orderID': f"{order}"},
                                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        return Response({'error': serializer.errors})


@api_view(['GET', 'PUT', 'DELETE'])
@login_required(login_url='/login/')
def order_view(request, slug):
    if request.method == 'GET':
        querySet = Order.objects.get(
            id=slug, buyer=request.user)
        serializer = OrderSerializer(querySet)
        # Get items in the order
        items = OrderItem.objects.filter(order=querySet)
        orderItem_serializer = OrderItemSerializer(items, many=True)
        return Response({'order': serializer.data, 'order Items': orderItem_serializer.data})
    elif request.method == 'PUT':
        order = Order.objects.get(id=slug)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid() and order.status != 'PRO':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "Invalid Request"},
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order = get_object_or_404(Order, id=slug)
        order.delete()
        return HttpResponseRedirect(reverse('orders_view'))
    else:
        return Response({'message': 'Unsupported HTTP method'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


'''
{
"cartItems": [
        { "productID": 1, "quantity": 2},
       { "productID": 5, "quantity": 2},
        { "productID": 10, "quantity": 1}
],
"total": 500
}
'''
