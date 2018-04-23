from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ghapp'
urlpatterns = [
	path('', views.index, name='index'),
	path('ghapp/system_preview/', views.system_preview, name='system_preview'),
	path('logout/', auth_views.logout, {'template_name':'ghapp/index.html'},name="logout"),
	path('login/', auth_views.login,{'template_name':'ghapp/login.html'}, name="login"),
]