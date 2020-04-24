from django.urls import path
from . import views

urlpatterns = [
    path('registration/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),


    path('', views.home,name="home"),
    path('products/',views.products,name="products"),
    path('customers/<str:pk_test>/',views.customers,name="customers"),
    path('village/',views.village),
    path('user/', views.userPage, name="user-page"),


    path('create_order/<str:pk_test>/',views.createOrder,name="create_order"),
    path('update_order/<str:pk_test>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk_test>/',views.deleteOrder,name="delete_order"),
]