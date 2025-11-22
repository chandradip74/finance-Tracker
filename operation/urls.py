from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('view_transaction/', views.view_transaction, name='view_transaction'),
    path('tran_analysis/', views.tran_analysis, name='tran_analysis'),
]