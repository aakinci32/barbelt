"""
URL configuration for BarBelt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views






urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeAction, name="homeAction"),
    path('facial/', views.facialRecognition, name="facialRecognition"),
    path('takePhoto/', views.takePhoto, name="takePhoto"),  
    path('login/', views.login_successful, name="login_successful"),
    path('savePhoto/', views.savePhoto, name="savePhoto"),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('products/', views.products, name='products'),
    path('submitRequest/', views.processRequest, name='submit_request'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('submitCart/', views.submitCart, name='submit_cart'),
]
