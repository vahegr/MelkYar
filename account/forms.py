from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "field", "placeholder": "گذرواژه"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "field", "placeholder": "تکرار گذرواژه"}))
    full_name = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'نام و نام خانوادگی'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'شماره مبایل'}))

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
        fields = ('phone', 'password', 'is_active', 'is_admin')


class LogInForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={}), validators=validators.MinLengthValidator(11))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "password-input", "placeholder": "گذرواژه"}))


# class EditProfileForm(forms.ModelForm):
#     full_name = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}))
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
#     phone = forms.CharField(
#         required=False,
#         max_length=11,
#         min_length=11,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'شماره مبایل'}))
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
#     bio = forms.CharField(
#         required=False,
#         widget=forms.Textarea(
#             attrs={'class': 'bio', 'placeholder': 'درباره'}))
#     instagram = forms.CharField(
#         required=False, widget=forms.URLInput(
#             attrs={'placeholder': 'آدرس اینستاگرام'}
#         ))
#     github = forms.CharField(
#         required=False,
#         widget=forms.URLInput(
#             attrs={'placeholder': 'آدرس گیتهاب'}
#         ))
#     linkedin = forms.CharField(
#         required=False,
#         widget=forms.URLInput(
#             attrs={'placeholder': 'آدرس لینکدین'}
#         ))
#     twitter = forms.CharField(
#         required=False,
#         widget=forms.URLInput(
#             attrs={'placeholder': 'آدرس توییتر'}
#         ))
#     image = forms.ImageField(required=False)
#
#     class Meta:
#         model = User
#         fields = ('full_name', 'email',
#                   'phone', 'username', 'bio', 'image',
#                   'instagram', 'github', 'linkedin', 'twitter')
