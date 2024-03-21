from django.urls import path
from .views import LoginView,Register,LogoutView,verify,editProfile,change_password,change_email,invoice,like_product,check_email,forgot_password,add_to_cart,cart,remove_cart,success,user_product,user_order


app_name = 'accounts'

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('register/',Register,name='register'),
    path('logout/',LogoutView, name='logout'),
    path('verify/<slug>',verify,name='verify'),
    path('editprofile/',editProfile,name='edit_profile'),
    path('change_password/',change_password,name="change_password"),
    path('change_email/',change_email,name="change_email"),
    path('check_email/',check_email,name="check_email"),
    path('forgot_password/<forgot_password_token>/',forgot_password,name="forgot_password"),
    path('cart/',cart,name="cart"),
    path('add-to-cart/<slug>/',add_to_cart,name="add_to_cart"),
    path('remove-cart/<slug>', remove_cart,name="remove_cart"),
    path('success/',success,name='success'),
    path('your_products/',user_product,name="your_products"),
    path('like-product/',like_product, name="like_product"),
    path('invoice/<order_id>',invoice, name="invoice"),
    path('your_orders/',user_order,name="your_orders"),
]
