from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from admin_action.models import Category
from .models import Transaction
from users.models import User
# Create your views here.

def dashboard(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'dashboard.html')




from django.contrib import messages

def add_transaction(request: HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")

    expense_categories = Category.objects.filter(type='Expense')
    income_categories = Category.objects.filter(type='Income')

    if request.method == "POST":
        user_id = request.COOKIES.get('userid')
        
        try:
            user = User.objects.get(userid=user_id)
        except User.DoesNotExist:
            return redirect("login")

        tran_type = request.POST.get("type")
        category = request.POST.get("category")
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        transaction = Transaction(
            userid=user,
            tran_type=tran_type,
            title=title,
            amount=amount,
            category=category,
            date=date
        )
        transaction.save()

        messages.success(request, "Transaction Added Successfully.")
        return redirect("view_transaction")  # <-- Redirect

    return render(request, 'add_transaction.html', {
        'expense_categories': expense_categories,
        'income_categories': income_categories,
    })





def view_transaction(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    user_id = request.COOKIES.get('userid')
    transaction = Transaction.objects.filter(userid = user_id)
    return render(request,'view_transaction.html',{ "transaction": transaction})


def tran_analysis(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'tran_analysis.html')