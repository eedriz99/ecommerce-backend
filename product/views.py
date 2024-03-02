from django.shortcuts import render
from django.http import response, HttpResponseRedirect
from utils.utils import login_required_for_non_get
from .serializer import CategorySerializer, ProductSerializer
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db import IntegrityError
# Create your views here.


@api_view(['GET', 'PUT', 'DELETE'])
@login_required_for_non_get
def product_view(request, slug):
    if request.method == 'GET':
        querySet = Product.objects.get(productID=int(slug))
        serializer = ProductSerializer(querySet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # get the object using its id and data given by client
        product = Product.objects.get(id=request.data['id'])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required_for_non_get
def products_view(request):
    if request.method == 'GET':
        querySet = Product.objects.all().order_by('productID')
        serializer = ProductSerializer(querySet, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # category = Category.objects.get_or_create(
        #     title=request.data["category"])[0].id
        # request.data['category'] = category
        # serializer = ProductSerializer(data=request.data)

        category = Category.objects.get_or_create(
            title=request.data['category'])[0]
        request.data['category'] = category
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect('/products/')
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
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


@api_view(['GET'])
def category_view(request):
    if request.method == 'GET':
        querySet = Category.objects.all()
        serializer = CategorySerializer(querySet, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
