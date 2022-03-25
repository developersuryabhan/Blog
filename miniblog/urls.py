
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='userlogout'),
    path('signup/', views.user_signup, name='usersignup'),
    path('login/', views.user_login, name='userlogin'),
    path('addpost/', views.add_poat, name='addpost'),
    path('updatepost/<int:id>/', views.update_poat, name='updatepost'),
    path('delete/<int:id>/', views.delete_poat, name='deletepost'),
]
