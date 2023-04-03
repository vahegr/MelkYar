from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as pass_views
from . import views

app_name = 'account'

urlpatterns = [
    path('main', views.main, name='main'),
    path('login', views.UserLogIn.as_view(), name='log in'),
    path('phone_confirm/<int:id>', views.chek_opt, name='phone_confirm'),
    path('logout', views.UserLogOut.as_view(), name='log out'),
    path('register', views.UserRegister.as_view(), name='register'),
]
