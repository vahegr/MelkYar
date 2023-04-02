from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as pass_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogIn.as_view(), name='log in'),
    path('logout', views.UserLogOut.as_view(), name='log out'),
    path('register', views.UserRegister.as_view(), name='register'),
    path(
        'activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate,
        name='activate'),
    re_path(r'profile/(?P<id>[0-9]+)/(?P<username>[-\w]+)/', views.user_panel, name='user_panel'),
    path(
        "password_reset/",
        pass_views.PasswordResetView.as_view(
            template_name="account/forgotpassword.html",
            email_template_name="account/password_reset_email.html",
            success_url=reverse_lazy("account:password_reset_done")
        ),
        name="password_reset"),
    path(
        "password_reset/done/",
        pass_views.PasswordResetDoneView.as_view(template_name="account/reset_password_done.html"),
        name="password_reset_done",),
    path(
        "reset/<uidb64>/<token>/",
        pass_views.PasswordResetConfirmView.as_view(
            template_name="account/reset-password.html",
            success_url=reverse_lazy("account:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        pass_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
        name="password_reset_complete",),
]
