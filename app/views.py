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


def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
      
        if not username or not password:
            messages.success(request,'Both Username and password are required')
            return redirect('/login/')
        # user_obj=User.objects.filter(username=username).first()
        # if user_obj is None:
        #     messages.success(request,'User not found.')
        #     return redirect('/login/')
        if (User.objects.filter(username=username).exists()):
            user=authenticate(request,username=username, password=password)
        else:
            user=User.objects.get(email=username)
            print(user)
            user=authenticate(username=user.username,password=password)
        if user is not None:
            login(request,user)
            # messages.success(request,f"You are logged in as {username}")
            return redirect('/dashboard/')
        else:
            messages.success(request,f"Invaild Credentials")
           


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
                messages.success(request,"Email is aldreay present.")
                return redirect('/register/')
            
            if password1!=password2:
                messages.success(request,"password and confirm password are not same")
                return redirect('/register/')
            else:
                data=User.objects.create_user(username=username,email=email,password=password1)
                data.save()
                profile_obj=Profile.objects.create(user=data)
                profile_obj.save()
                return redirect('/')
        except Exception as e:
            print(e)
    
    return render(request,'signup.html')


import uuid
def forget_password(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')
            email= request.POST.get("email")
            print(email)
            # print(username)
            if not User.objects.filter(email=email).first():
                messages.success(request,'User not found with this username.')
                return redirect('/forget-password/')
            user_obj=User.objects.get(email=email)
            print(user_obj)
            token=str(uuid.uuid4())
            profile_obj=Profile.objects.get(user=user_obj)
            print(profile_obj)
            profile_obj.forget_password_token=token
            profile_obj.save()
            print(user_obj)
            send_forget_password_mail(email,token)
            print(token)
            messages.success(request,'An email is sent')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)

    return render(request,'forget_password.html')

def change_password(request,token):
    context={}
    profile_obj=Profile.objects.filter(forget_password_token=token).first()
    print(profile_obj)
    if request.method=='POST':
        password1=request.POST['password']
        password2=request.POST['confirm_password']
        user_id=request.POST.get('user_id')
        if user_id is None:
            messages.success(request,"No user id found.")
            return redirect(f'/changep-passeord/{token}')
        if password1 != password2:
            messages.success(request,"both should be equal.")
            return redirect('/')
        user_obj=User.objects.get(id=user_id)
        user_obj.set_password(password1)
        user_obj.save()
        return redirect('/login/')
     
        
    context={'user_id':profile_obj.user.id}
    return render(request,'change-password.html',context)


def is_superuser(user):
    return user.is_superuser


# class PasswordChangeView(PasswordChangeView)



# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.core.signing import TimestampSigner

# def send_reset_password_email(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = get_user_model().objects.get(email=email)

#         if user:
#             # Generate a timestamped token for the user's email
#             timestamp = int(timezone.now().timestamp())
#             signer = TimestampSigner()
#             token = signer.sign_object({'email': email, 'timestamp': timestamp})

#             # Send the email with the reset link
#             reset_link = f'http://example.com/reset-password/?token={token}'
#             # Replace 'example.com' with your actual domain name
#             # Here, you can use Django's email sending mechanism or any third-party library.

#             return HttpResponse('Reset password link sent.')


# # views.py
# from django.core.signing import BadSignature, SignatureExpired

# def reset_password(request):
#     token = request.GET.get('token')
#     try:
#         signer = TimestampSigner()
#         data = signer.unsign_object(token, max_age=PASSWORD_RESET_TIMEOUT_DAYS * 24 * 3600)
#         email = data['email']
#         timestamp = data['timestamp']

#         # Check if the token is expired
#         if timezone.now().timestamp() - timestamp > PASSWORD_RESET_TIMEOUT_DAYS * 24 * 3600:
#             return HttpResponse('Reset password link has expired.')

#         # Process the password reset here
#         # ...

#         return HttpResponse('Password reset successful.')

#     except (BadSignature, SignatureExpired):
#         return HttpResponse('Invalid reset password link.')



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
            permissions = form.cleaned_data['permissions']

            if user:
                user.user_permissions.set(permissions)
            elif group:
                group.permissions.set(permissions)

            return render(request, 'success.html')
    else:
        form = AssignPermissionForm()

    return render(request, 'assign_permissions.html', {'form': form})