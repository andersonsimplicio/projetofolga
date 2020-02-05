from django.contrib import admin
from django.urls import path
from .views import home
from django.contrib import messages

urlpatterns = [
    path('', home, name='home'),
]
