from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'coordenador/login.html')
