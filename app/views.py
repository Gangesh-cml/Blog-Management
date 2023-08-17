from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from django.contrib import messages
from .models import Profile
from .helper import send_forget_password_mail
from .models import *
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings


def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if (User.objects.filter(username=username).exists()):
            user_obj=User.objects.filter(username=username).first()
            profile_obj=Profile.objects.filter(user=user_obj).first()
            user=authenticate(request,username=username, password=password)
        
        elif(User.objects.filter(email=username).exists()):
            user=User.objects.get(email=username)
            profile_obj=Profile.objects.filter(user=user).first()
            user=authenticate(username=user.username,password=password)
        
        else:
            messages.success(request,'User not found.')
            return redirect('/login/')


        if user.is_superuser:
            login(request,user)
            return redirect('/dashboard/')
        else:
            if not profile_obj.is_verified:
                messages.success(request,'profile is not verified please check your mail.')
                return redirect('/login')
            
        if user is not None:
            login(request,user)
            return redirect('/dashboard/')
        
        # else:
        #     messages.success(request,f"Invaild Credentials")
           


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
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is taken.')
                return redirect('/register/')
            if User.objects.filter(email=email).first():
                messages.success(request,"Email is aldreay present.")
                return redirect('/register/')
            
            if password1!=password2:
                messages.success(request,"password and confirm password are not same")
                return redirect('/register/')
            else:
                data=User.objects.create_user(username=username,email=email,password=password1)
                data.save()
                token=str(uuid.uuid4())
                profile_obj=Profile.objects.create(user=data , email_token=token)
                profile_obj.save()
                send_mail_after_registeration(email,token)
                return redirect('/login/')
        except Exception as e:
            print(e)
    
    return render(request,'signup.html')


import uuid
def forget_password(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')
            email= request.POST.get("email")
            if not User.objects.filter(email=email).first():
                messages.success(request,'User not found with this username.')
                return redirect('/forget-password/')
            user_obj=User.objects.get(email=email)
            token=str(uuid.uuid4())
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token=token
            profile_obj.save()
            send_forget_password_mail(email,token)
            messages.success(request,'An email is sent')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)

    return render(request,'forget_password.html')



def change_password(request,token):
    context={}
    profile_obj=Profile.objects.filter(forget_password_token=token).first()
    if request.method=='POST':
        password1=request.POST['password']
        password2=request.POST['confirm_password']
        user_id=request.POST.get('user_id')
        if user_id is None:
            messages.success(request,"No user id found.")
            return redirect(f'/change-passeord/{token}')
        if password1 != password2:
            messages.success(request,"both should be equal.")
            return redirect('/')
        user_obj=User.objects.get(id=user_id)
        user_obj.set_password(password1)
        user_obj.save()
        return redirect('/login/')
     
        
    context={'user_id':profile_obj.user.id}
    return render(request,'change-password.html',context)



#for mail verification

def send_mail_after_registeration(email,token):
    subject='your forget password link'
    message=f'hi,click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True

def verify(request, email_token):
    try:
        Profile_obj=Profile.objects.filter(email_token=email_token).first()
        if Profile_obj:
            if Profile_obj.is_verified:
                messages.success(request,'your acoount is already verified')
                return redirect('/login/')
            
            Profile_obj.is_verified = True
            Profile_obj.save()
            messages.success(request,'your acoount has been verified')
            return redirect('/login/')
        else:
            return messages.success(request,'link is invailid')
    except Exception as e :
        print(e)



def is_superuser(user):
    return user.is_superuser


from django.shortcuts import render
from .forms import AssignPermissionForm


def assign_permission_view(request):
    if request.method == 'POST':
        form = AssignPermissionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            print(group)
            permissions = form.cleaned_data['permissions']

            if user:
                user.user_permissions.set(permissions)
            if group:
                
                group1= Group.objects.get(name=group)
                user.groups.add(group1)
                group.permissions.set(permissions)

            return render(request, 'success.html')
    else:
        form = AssignPermissionForm()

    return render(request, 'assign_permissions.html', {'form': form})