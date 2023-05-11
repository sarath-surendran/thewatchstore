from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile, name="profile"),
    path('view_address/',views.view_address,name="view_address"),
    path('view_address/edit_address/<int:address_id>',views.edit_address,name="edit_address"),
    path('view_address/delete_address/<int:address_id>',views.delete_address,name="delete_address"),
    path('edit_user_profile<int:user_id>',views.edit_user_profile,name="edit_user_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('view_orders',views.view_orders,name="view_orders"),
    path('view_order_details/<int:id>',views.view_order_details, name="view_order_details"),
    path('cancel_order/<int:order_number>',views.cancel_order,name="cancel_order"),

]