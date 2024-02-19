"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from product import views as productViews
from order import views as orderViews
from userProfile import views as authViews

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # OAuth
    path('/auth/', include('drf_social_oauth2.urls', namespace='drf')),

    # Simple DRF-JWT urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user-defined URLS and views
    path('product/<slug:slug>/', productViews.product_view,
         name='product-detail-view'),
    path('products/', productViews.products_view, name='products-list-view'),
    path('paginatedproducts/', productViews.products_paginated_view,
         name='products-paginated-view'),
    path('category/', productViews.category_view, name='category-view'),
    path('orders/', orderViews.orders_view, name='order-list-view'),
    path('order/<slug:slug>', orderViews.order_view, name='order-detail-view'),
    path('register/', authViews.register, name='register-view'),
    path('login/', authViews.user_login, name='login-view'),
    path('logout/', authViews.user_logout, name='logout-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
