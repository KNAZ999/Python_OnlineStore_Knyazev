from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users_auth'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        success_url='users_auth:home'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html',
        next_page='users_auth:home'
    ), name='logout'),
]