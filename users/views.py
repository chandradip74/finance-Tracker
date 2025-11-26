from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
import re
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from operation.views import dashboard
# Create your views here.

def validemail(email: str) -> bool:
  pattern = "^([A-Za-z0-9]+[_\\-.]?)+[A-Za-z0-9]+@[A-Za-z0-9]+[.]?[A-Za-z0-9]+\\.[A-Za-z]+$"
  match = re.search(pattern, email)
  
  return match is not None


def validpassword(password: str) -> bool:
  if len(password) < 8:
    return False

  capital_pattern = "[A-Z]+"
  if re.search(capital_pattern, password) is None:
    return False
  
  small_pattern = "[a-z]+"
  if re.search(small_pattern, password) is None:
    return False
  
  number_pattern = "[0-9]+"
  if re.search(number_pattern, password) is None:
    return False
  
  special_char = "\\W+"
  if re.search(special_char, password) is None:
    return False

  return True
                            
  

def login(request :HttpRequest):
    if request.method == "GET":
        if request.COOKIES.get('email'):
            return redirect("dashboard")
        return render(request,"login.html")
    
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = User.objects.filter(email = email)

    if user.count == 0 :
       return render(request, {'error':'Wrong Email Or Password..'})
   
    user = user.first()
    passwordmatch = check_password(password, user.password)
    if not passwordmatch:
       return render(request,"login.html", {'error':'Wrong Email Or Password..'})
    
    response = redirect("dashboard")
    response.set_cookie('email', email)
    response.set_cookie('userid',user.userid)
    response.set_cookie('username', user.username)
    response.set_cookie('userrole', user.userrole)
    return response
          
    
def singup(request:HttpRequest):
    if request.method == "GET":
      if request.COOKIES.get('email') is not None:
          return redirect("dashboard")
      return render(request,"signup.html")
    
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirmpassword = request.POST.get("confirmpassword")

    if password != confirmpassword:
        return render(request,"signup.html",{'error':"Password and ConfirmPassword Not match"})
    
    valid_email = validemail(email)
    if not valid_email:
        return render(request,"signup.html",{'error':'Email is not valid'})
    
    valid_password = validpassword(password)
    if not valid_password:
        return render(request,"signup.html",{'error':'Password must be more than 8 characters and must contain at least one capital, small, number, and special characters'})


    emailexist = User.objects.filter(email = email)

    if emailexist.count() > 0:
       return render(request,"signup.html",{'error':'Email Alredy Exiest'})
    
    user_role = "user"
    hashpassword = make_password(password)

    User.objects.create(
       username = username,
       email = email,
       password = hashpassword,
       userrole = user_role
    )

    return redirect("login")
def logout(request:HttpRequest):
    response = redirect("login")
    response.delete_cookie('email')
    return response