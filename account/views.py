import requests
import ghasedakpack
import random
import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy
from melkyar import settings
from django.views import View
from django.views.generic import DetailView, CreateView
from .forms import LogInForm, UserCreationForm
from .models import User, Plan, ConfirmationCode, SerialNumber, Opt


def create_serial_number(request):
    create_number = ''.join(random.choices('0123456789', k=15))
    SerialNumber.objects.create(user_id=request.user.id, number=create_number)
    if SerialNumber.objects.filter(user_id=request.user.id, number=create_number).exists():
        create_number = ''.join(random.choices('0123456789', k=15))
        SerialNumber.objects.create(user_id=request.user.id, number=create_number)
    return redirect('panel')


def create_confirmation_code(request, number):
    serial_number = SerialNumber.objects.get(serial_number=number)
    create_code = uuid.uuid4()
    ConfirmationCode.objects.create(code=create_code, serial_number=number)
    serial_number_code = serial_number.code
    return render(request, '', context={'serial_number_code': serial_number_code})


class UserRegister(CreateView):
    form_class = UserCreationForm
    template_name = "account/register.html"
    success_url = reverse_lazy('home:home')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:home')
        return super(UserRegister, self).get(*args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        api = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
        num = random.randint(10000, 99999)
        Opt.objects.create(phone=cd['phone'], code=num)
        api.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': num})
        return render(self.request, "account/email_sent.html")  # render to confirm account with code


class UserLogIn(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            return redirect('home:home')
        form = LogInForm()
        return render(request, 'account/login.html', context={'form': form})

    def post(self, request):
        if request.user.is_authenticated is True:
            return redirect('home:home')
        form = LogInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
            else:
                form.add_error('email', 'اطلاعات وارد شده اشتباه است')
        else:
            form.add_error('email', 'اطلاعات وارد شده اشتباه است')

        return render(request, 'account/login.html', context={'form': form})


class UserLogOut(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


def user_panel(request, id, username):
    user = User.objects.get(id=id, username=username)
    return render(request, "account/user-panel.html", context={'object': user})


#  SUBSCRIPTION PAYMENT
def subscription(request, id, serial_number):
    # retrieve a list of available subscription plans from the database
    plans = Plan.objects.all()

    if request.method == 'POST':
        # retrieve the selected subscription plan from the form data
        selected_plan = Plan.objects.get(id=id)

        # generate a payment request on ZarinPal using their API
        response = requests.post('https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json', data={
            'MerchantID': 'your_merchant_id',
            'Amount': selected_plan.price,
            'Description': selected_plan.title,
            'Email': request.user.email,
            'CallbackURL': '/payment_callback/'  # this is redirect to create confirmation code page
        })

        # check if the payment request was successful
        if response.status_code == 200 and response.json().get('Status') == 100:
            # redirect the user to the payment link
            return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + response.json().get('Authority'))
        else:
            # display an error message
            return render(request, 'subscription.html', {'plans': plans, 'error': 'Error generating payment request'})

    # if the request method is GET, display the list of available subscription plans
    return render(request, 'subscription.html', {'plans': plans})
