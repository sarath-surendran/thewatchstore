from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('signin',views.login, name="login"),
    path('register',views.register, name="register"),
    #path('user_account',views.user_account, name="user_account"),
    path('user/add_address',views.add_address,name="add_address"),
    path('logout',views.logout,name="logout"),
    path('verify_register',views.verify_register, name="verify_register"),
    path('phone_login',views.phone_login,name="phone_login"),
    path('verify_login',views.verify_login,name="verify_login"),
    path('product_detail/<int:id>',views.product_details,name="product_detail"),
    path('forgot_password',views.forgot_password, name="forgot_password"),
    path('verify_reset_otp',views.verify_reset_otp, name="verify_reset_otp"),
    path('reset_password',views.reset_password,name='reset_password'),
    path('category/<str:cat_name>',views.category_wise_listing, name="category_wise_listing"),

]