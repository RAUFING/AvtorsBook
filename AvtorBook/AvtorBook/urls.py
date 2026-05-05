"""AvtorBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from catalog import views

urlpatterns = [
    re_path(r'^login/', views.login),
    re_path(r'^register/', views.register),
    re_path(r'^logout/', views.logout),
    re_path(r'^create_book/', views.addbook),
    re_path(r'^delpage/', views.delete_page),
    re_path(r'^datasession/', views.admin),
    re_path(r'^potv/', views.potv),
    re_path(r'^profiles/', views.profilespage),
    path('allbook/<str:name>', views.view_all_book),
    path('book/<str:id>', views.view_book),
    path('edit_book/<str:id>', views.editbook),
    path('main/<str:strtext>', views.str_mess),
    path('edit_profile/', views.editprofile),
    path('delete_book/<str:id>', views.deletebook),
    path('profile/<str:username>', views.view_profile),
    path('book_filter/<str:name>', views.filter_book),
    path('profile_filter/<str:name>', views.filter_profile),
    path('', views.index),
    path('admin/', admin.site.urls),
]
