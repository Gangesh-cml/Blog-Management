from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from django.contrib import messages
from .models import Profile
from .helper import send_forget_password_mail
# Create your views here.

def home(request):
    return render(request,'home.html')
def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if not username or not password:
            messages.success(request,'Both Username and password are required')
            return redirect('/login/')
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'User not found.')
            return redirect('/login/')

        user=authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f"You are logged in as {username}")
            return redirect("home")
        
        else:
            messages.success(request,("There was An Error Logging In,Try Again...."))

    return render(request,'loginpage.html')

# this function is used to logout the user
def logout_user(request):
    logout(request)
    print('hello')
    messages.success(request,("You Were Successfully logout"))
    return redirect('login')

# this function is used to register the new user
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        print(username)
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is taken.')
                return redirect('/register/')
            if User.objects.filter(email=email).first():
                messages.success(request,"Email is taken.")
                return redirect('/register/')
            
            if password1!=password2:
                messages.success(request,"password and confirm password are not same")
                return redirect('/register/')
            else:
                data=User.objects.create_user(username=username,email=email,password=password1)
                data.save()
                return redirect('login')
        except Exception as e:
            print(e)
    
    return render(request,'signup.html')
import uuid
def forget_password(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request,'User not found with this username.')
                return redirect('/forget-password/')
            user_obj=User.objects.get(username=username)
            token=str(uuid.uuid4())
            Profile_obj=Profile.objects.get(user = user_obj)
            Profile_obj.forget_password_token=token
            Profile_obj.save()
            send_forget_password_mail(user_obj,token)
            messages.success(request,'An email is sent')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)

    return render(request,'forget_password.html')

def change_password(request,token):
    context={}
    try:
        profile_obj=Profile.object.get(forget_password_token=token)
        print(profile_obj)  
    except Exception as e:
        print(e)

    return render(request,'change-password.html')

# class PasswordChangeView(PasswordChangeView)
