from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators
from .models import User, Plan, SerialNumber
from django.contrib.auth import password_validation


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-pill mt-4 input form-control w-50 mx-auto d-inline",
                "placeholder": "رمز عبور"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-pill mt-4 input form-control w-50 mx-auto d-inline",
                "placeholder": "تکرار رمز عبور"}))
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "rounded-pill mt-4 input form-control w-50 mx-auto d-inline",
                'placeholder': 'نام و نام خانوادگی'}))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "rounded-pill mt-4 input form-control w-50 mx-auto d-inline",
                'placeholder': 'شماره مبایل'}))

    class Meta:
        model = User
        fields = ('full_name', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("اختلافی در کلمه عبور وجود دارد")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'full_name', 'password', 'is_active', 'is_admin')


class LogInForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": 'rounded-pill mt-4 input form-control w-50 mx-auto d-inline',
                "placeholder": "شماره تلفن"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "rounded-pill mt-4 input form-control w-50 mx-auto d-inline",
                "placeholder": "رمز عبور"}))


class SubscriptionForm(forms.Form):
    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'rounded-pill mt-4 input form-control w-75 mx-auto'}),
        required=True,
    )
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.all(),
        to_field_name='title',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select mt-4 w-25 mx-auto'})
    )

    # def clean_serial_number(self, request):
    #     serial_number = self.cleaned_data.get('serial_number')
    #     serial_number_query = SerialNumber.objects.get(number=serial_number)
    #     serial_number_query_filter = SerialNumber.objects.filter(number=serial_number)
    #     if serial_number_query.user.id != request.user.id:
    #         raise ValidationError('این شماره سریال مال شما نیست!', code='wrong_serial_number')
    #     if not serial_number_query_filter.exists():
    #         raise ValidationError('این شماره سریال وجود ندارد!', code='serial_number_doesnt_exist')


class ChekOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'rounded-pill mt-4 input form-control w-75 mx-auto'}),
        required=True,
    )


class PasswordResetForm(forms.Form):

    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={
            "placeholder": "رمز عبور",
            'class': 'rounded-pill mt-4 input form-control w-75 mx-auto'
        }
    ))

    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={
            "placeholder": "تکرار رمز عبور",
            'class': 'rounded-pill mt-4 input form-control w-75 mx-auto'
        }
    ))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("اختلافی در کلمه عبور وجود دارد")
        return password2
