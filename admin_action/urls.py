from django.urls import path
from . import views
urlpatterns = [
   path('',views.admin_dashboard,name='admin_dashboard'),
   path('add_category/',views.add_category,name='add_category'),
   path('user_manage/',views.user_manage,name='user_manage'),
   path('category_manage/',views.category_manage,name='category_manage'),
   path('delete_category/<int:cat_id>/',views.delete_category,name="delete_category"),
   path('update_category/<int:cat_id>/',views.update_category,name="update_category"),
   path('delete_user/<int:user_id>/',views.delete_user,name="delete_user"),
   path('update_user/<int:user_id>/',views.update_user,name="update_user"),
]