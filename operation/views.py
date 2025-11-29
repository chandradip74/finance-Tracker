from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from admin_action.models import Category
from .models import Transaction
from users.models import User


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
        return redirect("view_transaction") 

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

    transaction = Transaction.objects.get(tran_id=tran_id)

    if request.method == "POST":
        transaction.tran_type = request.POST.get("type")
        transaction.title = request.POST.get("title")
        transaction.amount = request.POST.get("amount")
        transaction.category = request.POST.get("category")
        transaction.date = request.POST.get("date")
        transaction.save()

        messages.success(request, "Transaction Updated Successfully..")
        return redirect("view_transaction")

    categories = Category.objects.all()

    return render(request, "update_transaction.html", {
        "transaction": transaction,
        "categories": categories
    })

def tran_analysis(request:HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect("login")
    userid= request.COOKIES.get("userid")

    userdata = Transaction.objects.filter(userid = userid)
    incomecount = Transaction.objects.filter(userid = userid,tran_type ="Income").count()
    expensecount = Transaction.objects.filter(userid = userid,tran_type ="Expense").count()
    Max_Income = 0
    Max_Expense = 0
    Min_Expense = 0
    Min_Income = 0

    Average_Income = 0
    Average_Expense = 0
    Income_Amount = 0
    Expense_Amount = 0

    for i in userdata:
        if i.tran_type == "Income":
            Income_Amount += i.amount
        elif i.tran_type == "Expense":
            Expense_Amount += i.amount

    Average_Income = Income_Amount / incomecount if incomecount != 0 else 0
    Average_Expense = Expense_Amount / expensecount if expensecount != 0 else 0  

    for i in userdata:
        if i.tran_type == "Income":
            if i.amount > Max_Income:
                Max_Income = i.amount
        
            if i.amount < Max_Income:
                Min_Income = i.amount

    
    for i in userdata:
        if i.tran_type == "Expense":
            if i.amount > Max_Expense:
                Max_Expense = i.amount

            if i.amount < Max_Expense:
                Min_Expense = i.amount

    return render(request,'tran_analysis.html',{"incomecount":incomecount,
                                                "expensecount":expensecount,
                                                "Average_Income":Average_Income,
                                                "Average_Expense":Average_Expense,
                                                "Max_Income":Max_Income,
                                                "Min_Income":Min_Income,
                                                "Max_Expense":Max_Expense,
                                                "Min_Expense":Min_Expense})