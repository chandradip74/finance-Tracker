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
    userid= request.COOKIES.get("userid")
    totalincome = 0
    totalexpense = 0
    netbalance = 0
    userdata = Transaction.objects.filter(userid = userid).order_by("-date")

    for u in userdata:
        if u.tran_type == "Income":
            totalincome += u.amount

    for u in userdata:
        if u.tran_type == "Expense":
            totalexpense += u.amount

    netbalance = totalincome - totalexpense
    return render(request,'dashboard.html',{"userdata":userdata,
                                            "totalincome":totalincome,
                                            "totalexpense":totalexpense,
                                            "netbalance":netbalance})


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

def delete_transaction(request:HttpRequest,tran_id:int):
     if request.COOKIES.get('email') is None:
        return redirect("login")
     
     transaction = Transaction.objects.filter(tran_id = tran_id)
     transaction.delete()
     messages.success(request,"Transaction Deleted Successfully..")
     return redirect("view_transaction")


def update_transaction(request: HttpRequest, tran_id: int):
    if request.COOKIES.get('email') is None:
        return redirect("login")

    # Fetch the single transaction
    transaction = Transaction.objects.get(tran_id=tran_id)

    # Fetch categories for dropdown
    category = Category.objects.all()

    if request.method == "POST":
        transaction.tran_type = request.POST.get("type")
        transaction.title = request.POST.get("title")
        transaction.amount = request.POST.get("amount")
        transaction.category_id = request.POST.get("category")   # foreign key
        transaction.date = request.POST.get("date")

        transaction.save()

        messages.success(request, "Transaction Updated Successfully..")
        return redirect("view_transaction")

    return render(request, "update_transaction.html", {
        "transaction": transaction,
        "category": category
    })


def tran_analysis(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    return render(request,'tran_analysis.html')