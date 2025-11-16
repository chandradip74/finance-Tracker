from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest

# Create your views here.

def home(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'home.html')
