from django.urls import path
from . import views


urlpatterns = [
    path('place_order',views.place_order,name="place_order"),
    path('place_order_online',views.place_order_online,name="place_order_online"),
    path('proceed_to_pay',views.razorpaycheck,name="razorpaycheck"),
    path('order_confirmation/',views.order_confirmation,name="order_confirmation"),
    # path('order_confirmation/<int:order_number>/<int:total>',views.order_confirmation,name="order_confirmation"),

]