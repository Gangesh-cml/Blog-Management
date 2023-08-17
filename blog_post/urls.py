from django.urls import path
from blog_post import views

urlpatterns = [
    path('',views.home,name='home'),
    path('add/',views.add_post,name='blog'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('edit/<id>/',views.edit_post,name='edit_profile'),
    path('regular_user/',views.dashboard1,name='dashboard1'),
    path('about/',views.about,name='about'),
    path('dashboard/edit/<id>/',views.edit_post,name='edit'),
    path('dashboard/delete/<id>/',views.delete_post,name='delete'),
    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('know/<id>/',views.know,name='know'),
    path('likes/<int:pk>/',views.likeview,name='likes'),
    path('comments/<int:pk>/',views.comments,name='comments')
   
]