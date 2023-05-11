from django.urls import path
from . import views

urlpatterns = [
    path('',views.category_management,name='admin_category_management'),
    path('add_category',views.add_category,name="admin_add_category"),
    path('edit_category',views.edit_category, name="edit_category"),
    path('admin_edit_category',views.save_category,name="admin_edit_category"),
    path('delete_category',views.delete_category, name="delete_category"),
]