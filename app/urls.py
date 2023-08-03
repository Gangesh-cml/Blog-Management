from django.urls import path
from app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register,name='register'),
    path('forget-password/',views.forget_password,name='forget-password'),
    path('change-password/<token>/',views.change_password,name='change-password'),
]