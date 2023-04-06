import requests
import ghasedakpack
import random
import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from melkyar import settings
from django.views import View
from django.views.generic import DetailView, CreateView
from .forms import LogInForm, UserCreationForm, SubscriptionForm, ChekOtpForm, PasswordResetForm
from .models import User, Plan, ConfirmationCode, SerialNumber, Opt


class UserRegister(CreateView):
    form_class = UserCreationForm
    template_name = "account/register.html"
    success_url = reverse_lazy('account:main')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account:main')
        return super(UserRegister, self).get(*args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        cd = form.cleaned_data
        api = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
        num = random.randint(10000, 99999)
        Opt.objects.create(phone=cd['phone'], code=num)
        api.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': num})
        print(num)
        opt = Opt.objects.get(phone=cd['phone'], code=num)

        return redirect(reverse_lazy('account:phone_confirm', kwargs={'id': opt.id}))


def chek_otp(request, id):
    if request.method == 'POST':
        form = ChekOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Opt.objects.filter(code=cd['code'], id=id).exists():
                opt = Opt.objects.get(code=cd['code'], id=id)
                user = User.objects.get(phone=opt.phone)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('account:main')
            else:
                form.add_error('code', 'کد وارد شده اشتباه است !')
        return render(request, 'account/confirm_phone.html', context={'form': form})


class UserLogIn(View):
    def get(self, request):
        if request.user.is_authenticated is True:
            return redirect('account:main')
        form = LogInForm()
        return render(request, 'account/login.html', context={'form': form})

    def post(self, request):
        if request.user.is_authenticated is True:
            return redirect('account:main')
        form = LogInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('account:main')
            else:
                form.add_error('phone', 'اطلاعات وارد شده اشتباه است')
        else:
            form.add_error('phone', 'اطلاعات وارد شده اشتباه است')

        return render(request, 'account/login.html', context={'form': form})


class UserLogOut(View):
    def get(self, request):
        logout(request)
        return redirect('account:log in')


def forgot_password(request):
    context = {"errors": []}
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if User.objects.filter(phone=phone).exists():
            api = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
            num = random.randint(10000, 99999)
            Opt.objects.create(phone=phone, code=num)
            api.verification({'receptor': phone, 'type': '1', 'template': 'randcode', 'param1': num})
            print(num)
            opt = Opt.objects.get(phone=phone, code=num)
            return redirect(reverse('account:enter_code', kwargs={'id': opt.id}))
        else:
            context["errors"].append('کاربری با شماره وارد شده وجود ندارد !')
    return render(request, 'account/forgot_password.html', context)


def otp_for_reset_password(request, id):
    form = ChekOtpForm()
    if request.method == 'POST':
        form = ChekOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Opt.objects.filter(code=cd['code'], id=id).exists():
                otp = Opt.objects.get(code=cd['code'], id=id)
                return HttpResponseRedirect(reverse('account:reset_password', kwargs={'id': otp.id}))
            else:
                form.add_error('code', 'کد وارد شده اشتباه است !')
        return HttpResponse('not found')
    return render(request, 'account/confirm_phone.html', context={'form': form})


def reset_password(request, id):
    otp_filter = Opt.objects.filter(id=id)
    otp = Opt.objects.get(id=id)
    user = User.objects.get(phone=otp.phone)
    form = PasswordResetForm()
    if otp_filter.exists():
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get("new_password1")
                user.set_password(password1)
                user.save()
                otp.delete()
                return HttpResponseRedirect(reverse('account:log in'))
            else:
                return form.errors
        return render(request, 'account/reset_password.html', context={'form': form})


def user_panel(request):
    if request.user.is_authenticated:
        user_serial_numbers = SerialNumber.objects.filter(user_id=request.user.id)
        return render(request, "account/userpanel.html", context={'serial_numbers': user_serial_numbers})
    else:
        return redirect('account:log in')


# def subscription(request, id, serial_number):
#     # retrieve a list of available subscription plans from the database
#     plans = Plan.objects.all()
#
#     if request.method == 'POST':
#         # retrieve the selected subscription plan from the form data
#         selected_plan = Plan.objects.get(id=id)
#
#         # generate a payment request on ZarinPal using their API
#         response = requests.post('https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json', data={
#             'MerchantID': 'your_merchant_id',
#             'Amount': selected_plan.price,
#             'Description': selected_plan.title,
#             'Email': request.user.email,
#             'CallbackURL': '/payment_callback/'  # this is redirect to create confirmation code page
#         })
#
#         # check if the payment request was successful
#         if response.status_code == 200 and response.json().get('Status') == 100:
#             # redirect the user to the payment link
#             return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + response.json().get('Authority'))
#         else:
#             # display an error message
#             return render(request, 'subscription.html', {'plans': plans, 'error': 'Error generating payment request'})
#
#     # if the request method is GET, display the list of available subscription plans
#     return render(request, 'subscription.html', {'plans': plans})


def create_serial_number(request):
    if request.user.is_authenticated:
        create_number = ''.join(random.choices('0123456789', k=15))
        SerialNumber.objects.create(user_id=request.user.id, number=create_number)
        return redirect('account:user_panel')
    else:
        redirect('account:log in')


def main(request):
    form = SubscriptionForm()
    user_serial_numbers = SerialNumber.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            plan = Plan.objects.get(title=cd['plan'])
            if SerialNumber.objects.filter(number=cd['serial_number']).exists():
                serial_number = SerialNumber.objects.get(number=cd['serial_number'])
                if serial_number.user.id != request.user.id:
                    form.add_error('serial_number', 'این شماره سریال مال شما نیست !')
                else:
                    return redirect(reverse('account:create_confirmation_code',
                                            kwargs={'plan_id': plan.id, 'serial_number_id': serial_number.id}))
            else:
                form.add_error('serial_number', 'این شماره سریال وجود ندارد !')
        else:
            form.add_error('serial_number', 'اطلاعات وارد شده اشتباه است')
    return render(request, 'account/main.html', context={'serial_numbers': user_serial_numbers, 'form': form})


def create_confirmation_code(request, plan_id, serial_number_id):
    if request.user.is_authenticated:
        serial_number = SerialNumber.objects.get(id=serial_number_id)
        plan = Plan.objects.get(id=plan_id)
        serial_number.days_charge += plan.days
        serial_number.save()
        create_code = uuid.uuid4()
        exist_code = ConfirmationCode.objects.filter(serial_number=serial_number)
        if exist_code.exists():
            confirmation_code = ConfirmationCode.objects.get(serial_number=serial_number)
            confirmation_code.code = create_code
            confirmation_code.save()
        else:
            ConfirmationCode.objects.create(code=create_code, serial_number_id=serial_number.id)
        return redirect(reverse('account:get_code', kwargs={'id': serial_number.id}))
    else:
        return redirect('account:log in')


def get_code(request, id):
    if request.user.is_authenticated:
        serial_number = SerialNumber.objects.get(id=id)
        if serial_number.user.id == request.user.id:
            return render(request, 'account/get_code.html', context={'serial_number': serial_number})
        else:
            return redirect('account:main')
    else:
        return redirect('account:log in')
