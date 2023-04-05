from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as pass_views
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.main, name='main'),
    path('create_serial_number', views.create_serial_number, name='create_serial_number'),
    path('create_confirmation_code/<int:plan_id>/<int:serial_number_id>', views.create_confirmation_code, name='create_confirmation_code'),
    path('get_code/<int:id>', views.get_code, name='get_code'),
    path('panel', views.user_panel, name='user_panel'),
    path('login', views.UserLogIn.as_view(), name='log in'),
    path('phone_confirm/<int:id>', views.chek_otp, name='phone_confirm'),
    path('logout', views.UserLogOut.as_view(), name='log out'),
    path('register', views.UserRegister.as_view(), name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('enter_code/<int:id>', views.otp_for_reset_password, name='enter_code'),
    path('reset_password/<int:id>', views.reset_password, name='reset_password'),
]
