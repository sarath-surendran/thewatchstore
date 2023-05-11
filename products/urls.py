from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_management,name='admin_product_management'),
    path('add_product',views.add_product,name="admin_add_product"),
    path('delete_product',views.delete_product,name="delete_product"),
    path('edit_product',views.edit_product,name="edit_product"),
    path('edit_product_save',views.edit_product_save,name="edit_product_save"),
]