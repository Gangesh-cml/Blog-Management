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
                return redirect('/')
        except Exception as e:
            print(e)
    
    return render(request,'signup.html')
import uuid
def forget_password(request):
    try:
        if request.method=='POST':
            # username=request.POST.get('username')
            email= request.POST.get("email")
            print(email)
            # print(username)
            if not User.objects.filter(email=email).first():
                messages.success(request,'User not found with this username.')
                return redirect('/forget-password/')
            user_obj=User.objects.get(email=email)
            token=str(uuid.uuid4())
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
    try:
        profile_obj=Profile.object.get(forget_password_token=token)
        print(profile_obj)  
    except Exception as e:
        print(e)

    return render(request,'change-password.html')

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
