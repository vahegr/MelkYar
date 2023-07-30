from django.urls import path, include, re_path
from . import views

app_name = 'api'

urlpatterns = [
    path('serial_numbers', views.SerialNumbersView.as_view(), name='serial_numbers'),
    path('get_serial_number/<str:number>', views.SerialNumberDetailView.as_view(), name='get_serial_number'),
    path('confirmation_codes', views.ConfirmationCodesView.as_view(), name='confirmation_codes'),
    path('create_code', views.CreateCodeView.as_view(), name='create_code'),
]
