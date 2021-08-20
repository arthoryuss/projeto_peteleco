from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name='peteleco'

urlpatterns = [
    path("",  LoginView.as_view(template_name = 'login.html'), 
    	 name='login'),
    path('logout/', LogoutView.as_view(next_page= 'peteleco:login'), 
    	 name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("teste/", views.teste, name='teste'),
]