from django.shortcuts import render
from django.http import response
from .serializer import CategorySerializer, ProductSerializer
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_view(request, slug):
    if request.method == 'GET':
        querySet = Product.objects.get(productID=int(slug))
        serializer = ProductSerializer(querySet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED
                            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # get the object using its id and data given by client
        product = Product.objects.get(id=request.data['id'])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def products_view(request):
    if request.method == 'GET':
        querySet = Product.objects.all().order_by('productID')
        serializer = ProductSerializer(querySet, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def products_paginated_view(request):
    if request.method == 'GET':
        querySet = Product.objects.all().order_by('productID')
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(querySet, request)

        if result is not None:
            serializer = ProductSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def category_view(request):
    if request.method == 'GET':
        querySet = Category.objects.all()
        serializer = CategorySerializer(querySet, many=True)
        return Response(serializer.data)
