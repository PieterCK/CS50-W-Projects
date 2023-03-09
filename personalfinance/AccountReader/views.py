from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "AccountReader/index.html")

def login(request):
    return render(request, "AccountReader/login.html")

def logout(request):
    return render(request, "AccountReader/login.html")

def register(request):
    return render(request, "AccountReader/login.html")