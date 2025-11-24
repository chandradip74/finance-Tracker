from django.urls import path
from . import views
urlpatterns = [
   path('',views.admin_dashboard,name='admin_dashboard'),
   path('add_category/',views.add_category,name='add_category'),
   path('user_manage/',views.user_manage,name='user_manage'),
   path('category_manage/',views.category_manage,name='category_manage'),
]