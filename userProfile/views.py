from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import JsonResponse


from .serializer import RegistrationSerializer, LoginSerializer


from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def user_logout(request):
    logout(request)
    return redirect('/login/')


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
            # return Response(redirect('/login/'), status=status.HTTP_202_ACCEPTED)
            return redirect('/login/')
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
                    print(request)

                    response = {'message': f"login {email} successful"}

                    # refresh = RefreshToken.for_user(user, user_id=user.email)
                    # return Response({
                    #     'access_token': str(refresh.access_token),
                    #     'refresh_token': str(refresh),
                    # })

                    # return redirect('/products/')

                    # next_url = request.GET.get(
                    #     'next', reverse('products-list-view'))
                    # return redirect(next_url)
                except Exception as e:
                    response = {'error': str(e)}
            return Response(response)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


"""{
    "firstname": "iDris",
    "lastname": "Akin",
    "email": "akinsola.ia@gmail.com",
    "password": "[Biu4W@R]"
}
"""
