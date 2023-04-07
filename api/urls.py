from django.urls import path, include, re_path
from . import views

app_name = 'api'

urlpatterns = [
    path('serial_numbers', views.SerialNumbersView.as_view(), name='serial_numbers'),
    path('confirmation_codes', views.ConfirmationCodesView.as_view(), name='confirmation_codes'),
]
