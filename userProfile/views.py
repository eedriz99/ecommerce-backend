from django.shortcuts import render

from rest_framework.decorators import api_view
# Create your views here.


@api_view(methods=['POST'])
def register(request):
    pass


@api_view(methods=['POST'])
def login(request):
    pass
