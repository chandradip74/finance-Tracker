from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def admin_dashboard(request: HttpRequest):
    return render(request, 'admin_dashboard.html')
