"""test_qx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rbac import views
from main import views as main

urlpatterns = [
    path('', views.Login),
    path('register/', views.Register),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('index/', main.index),
    path('student_page/', main.get_student_page),
    path('book_page/', main.get_book_page),
    path('student/', main.student),
    path('book/', main.book),
    path('rbac/permission/', views.Permission),
    path('rbac/user/', views.MyUser),
    path('rbac/role/', views.MyRole),
    path('rbac/permission_menu/', views.MyMenu),
]

