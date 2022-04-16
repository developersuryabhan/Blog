from imaplib import _Authenticator
import imp
from tokenize import group
from turtle import title
from unicodedata import name
from django.shortcuts import render, HttpResponseRedirect
from .forms import SingnUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.paginator import Paginator
from .models import Post


# Home Function
def home(request):
    posts =Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

# About Function
def about(request):
    return render(request, 'blog/about.html')

# Contact Function
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard Function
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('id')
        user = request.user
        full_name = user.get_full_name()
        gps =user.groups.all()
        ip = request.session.get('ip', 0)
        count=cache.get('count', version = user.pk)
        paginator = Paginator(posts, 3, orphans=1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/dashboard.html', {'page_obj':page_obj , 'full_name':full_name, 'groups':gps, 'ip':ip, 'count': count})
    else:
        return HttpResponseRedirect('/login/')


# Logout Function
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup Function
def user_signup(request):
    if request.method == "POST":
        form = SingnUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations!! You Have Become an Author.")
            user = form.save()
            form = SingnUpForm()
            group = Group.objects.get(name='Author')
            user.groups.add(group)

    else:
        form = SingnUpForm()
    return render(request, 'blog/signup.html', {'form': form})

# Login Function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upassword = form.cleaned_data['password']
                user = authenticate(username=uname, password=upassword)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add New Post Function
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                 title= form.cleaned_data['title']
                 description = form.cleaned_data['description']
                 posts = Post(title=title, description=description)
                 posts.save()
                 messages.success(request, 'Add Post in Successfully !!')
                #  form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update Post Function
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update post in Successfully !!')
                form = PostForm()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# delete Post Function
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request, 'Delete Post in Successfully !!')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


