from django.urls import path
from app import views


urlpatterns = [
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register,name='register'),
    path('forget-password/',views.forget_password,name='forget-password'),
    path('change-password/<token>/',views.change_password,name='change-password'),
    path('assign_permissions/', views.assign_permission_view, name='assign_permissions'),
    path('verify/<email_token>',views.verify,name='verify')
]