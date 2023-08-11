from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import PasswordChangeView

from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Permission

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_regular_user(user):
    return user.groups.filter(name='Regular_User').exists()


def home(request):
    posts=BlogModel.objects.all()
    print(posts)
    data={
        'data':posts
    }
    return render(request,'home.html',data)

# @login_required
# def regular_user(request):
#     posts=BlogModel.objects.all()
#     print(posts)
#     data={
#         'data':posts
#     }
#     return render (request,'regular_user.html',data)

@login_required
def dashboard(request):
    posts=BlogModel.objects.all()
    print(posts)
    data={
        'data':posts
    }
    return render (request,'dashboard.html',data)

@login_required
def dashboard1(request):
    current_user=request.user
    user_id=current_user.id
    user_name=current_user.username
    print(user_name)
    # queryset=BlogModel.objects.get(author=user_name)
    # print(queryset.author)
    # if(user_name==queryset.author or current_user.is_superuser):
    data=User.objects.get(id=user_id)
    data1=BlogModel.objects.filter(author=data)
    print(data1)
    data={
        'data':data1
    }
    return render (request,'regular_dashboard.html',data)




@login_required(login_url='/login/')

def add_post(request):
    current_user=request.user
    user_id=current_user.id
    print(user_id)
    if request.method=="POST":
        data=request.POST
        title=request.POST['title']
        content=request.POST['content']
        image=request.POST['image']
        data=BlogModel.objects.create(title=title,content=content,image=image,author_id=user_id)
        data.save()
        return redirect('/dashboard/')

    return render(request,'post_form.html')

@login_required
def delete_post(request,id):
    current_user=request.user
    user_id=current_user.id
    queryset=BlogModel.objects.get(id=id)
    print(queryset.author_id)
    if(user_id==queryset.author_id or current_user.is_superuser):
        queryset.delete()
    else:
        messages.success(request,'You have not access of this functionality')
        return redirect('/dashboard')

    return redirect('/dashboard/')


def about(request):
    posts=BlogModel.objects.all()
    print(posts)
    data={
        'data':posts
    }
    return render(request,'about.html',data)


@login_required
def edit_post(request,id):
    current_user=request.user
    user_id=current_user.id
    queryset=BlogModel.objects.get(id=id)
    
    if user_id==queryset.author_id or current_user.is_superuser :
        if request.method=="POST":
            data=request.POST

            title=request.POST['title']
            content=request.POST['content']
            # image=request.POST['image']

            queryset.title=title
            queryset.content=content
            # queryset.image=image
            queryset.save()
            return redirect('/dashboard/')
    else:
        messages.success(request,'You have not access of this functionality')
        return redirect('/dashboard')

    context={
        'record':queryset
    }
    return render(request,'edit_post.html',context)

@login_required
def profile(request):
    current_user=request.user
    user_id=current_user.id
    user_name=current_user.username
    user_email=current_user.email
    
    queryset=User.objects.get(id=user_id)
    if request.method=="POST":
        data=request.POST

        Username=request.POST['Username']
        Email=request.POST['Email']
        password=request.POST['password']
        # slug=request.POST['slug']

          
        queryset.title=Username
        queryset.content=Email

        # queryset.slug=slug
        queryset.save()
        return redirect('/dashboard/')

    context={
        'record':queryset
    }
    return render(request,'profile.html',context)

@login_required
def edit_profile(request):
    current_user=request.user
    user_id=current_user.id
    data=request.current_user.hasp_perm()
    user_name=current_user.username
    user_email=current_user.email
   
    queryset=User.objects.get(id=user_id)
    
    if request.method=="POST":
        data=request.POST
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        Username=request.POST['Username']
        Email=request.POST['Email']

        queryset.first_name=firstname
        queryset.last_name=lastname
        queryset.username=Username
        queryset.email=Email

        queryset.save()
        return redirect('/dashboard/')

    context={
        'record':queryset
    }
    return render(request,'update_profile.html',context)

@login_required
def know(request,id):
    queryset=BlogModel.objects.get(id=id)
    context={
        'data':queryset
    }
    stuff=get_object_or_404(BlogModel,id=id)
    total_likes=stuff.total_likes()
    print(total_likes)
    context["total_likes"]=total_likes
    return render(request,'know.html',context)

@login_required
def likeview(request,pk):
    post=get_object_or_404(BlogModel,id=pk)
    post.likes.add(request.user)
    print(post)
    return redirect('/dashboard/')