from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from admin_action.models import Category
# Create your views here.

def dashboard(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'dashboard.html')


def add_transaction(request:HttpRequest):
     if request.COOKIES.get('email') is None:
        return redirect("login")
     
     category = Category.objects.all()
     return render(request,'add_transaction.html',{'category':category})


def view_transaction(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'view_transaction.html')


def tran_analysis(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'tran_analysis.html')