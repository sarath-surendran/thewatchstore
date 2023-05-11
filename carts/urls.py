from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart, name="cart"),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name="add_to_cart"),
    path('decrease_cart/<int:product_id>/<int:cart_item_id>',views.decrease_cart, name="decrease_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',views.remove_cart, name="remove_cart"),
    path('checkout',views.checkout,name="checkout"),
    path('verify_coupon',views.verify_coupon,name="verify_coupon"),
    path('remove_coupon',views.remove_coupon,name="remove_coupon"),
]