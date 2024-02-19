from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.response import Response

from .serializer import RegistrationSerializer, LoginSerializer


from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
# Create your views here.


@api_view(['GET'])
def user_logout(request):
    logout(request)
    return Response({'message': 'logged out'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def register(request):
    """ user registration view """
    if request.method == 'GET':
        logout(request)
        return Response({"message": 'Success'})
    elif request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_login(request):
    if request.method == 'GET':
        logout(request)
        return Response({"message": 'Success'})
    elif request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email,
                                password=password)
            response = {}
            if user is not None:
                try:
                    login(request, user)
                    # response = HttpResponseRedirect(reverse('orders_view'))
                    response = {'message': f"login {email} successful"}
                except Exception as e:
                    response = {'message': str(e)}
            return Response(response)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


"""{
    "firstname": "iDris",
    "lastname": "Akin",
    "email": "akinsola.ia@gmail.com",
    "password": "[Biu4W@R]"
}
"""
