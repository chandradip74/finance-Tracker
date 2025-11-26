from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Category
from users.models import User
# Create your views here.

def admin_dashboard(request: HttpRequest):
    if not request.COOKIES.get('email') or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")
    return render(request, 'admin_dashboard.html')

def add_category(request: HttpRequest):
    if request.COOKIES.get('email') is None or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")

    
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        category_type = request.POST.get('category_type')

        if category_name.isdigit():
            return render(request, "add_category.html", {"error": "Category not be number.Type valid name"})
    
        exist_category = Category.objects.filter(name=category_name, type=category_type).first()
        if exist_category:
            return render(request, "add_category.html", {"error": "Category already exists"})

    
        new_category = Category(name=category_name, type=category_type)
        new_category.save()

        return render(request, "add_category.html", {"success": "Category added successfully!"})

    return render(request, "add_category.html")

def user_manage(request: HttpRequest):
    if not request.COOKIES.get('email') or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")
    
    user = User.objects.all()
    return render(request, 'user_manage.html',{'user':user})


def category_manage(request: HttpRequest):
    if not request.COOKIES.get('email') or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")
    
    category = Category.objects.all()
    return render(request, 'category_manage.html',{'category':category})

def delete_category(request:HttpRequest, cat_id:int):
    if not request.COOKIES.get('email') or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")
     
    if cat_id:
        category = Category.objects.filter(cat_id = cat_id)
        category.delete()
    else:
        messages.error(request,"Category not Deleted")

    return redirect("category_manage")

def update_category(request:HttpRequest, cat_id:int):
    if not request.COOKIES.get('email') or request.COOKIES.get('userrole') != 'admin':
        return redirect("login")
    
    if cat_id:
        category = Category.objects.filter(cat_id = cat_id).first()
    else:
        return redirect("category_manage")
    
    if request.method == "POST":
        category.type = request.POST.get("category_type")
        category.name = request.POST.get("category_name")
        category.save()

        messages.success(request,"Category Updated Successfully.")
        return redirect("category_manage")
    
    return render(request,"update_category.html",{"category":category})
