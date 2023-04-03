from django.utils import timezone
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    full_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='نام و نام خانوادگی'
    )
    phone = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        verbose_name='شماره مبایل'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعالیت'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='ادمین'
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name', ]

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر ها'

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        " Is the user a member of staff? "
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Opt(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    activation_date = models.DateTimeField(auto_now_add=True)

    def check_status(self):
        now = timezone.now()
        end_day = self.activation_date.hour + 5
        if now > end_day:
            self.delete()
            self.save()
        return None


class Plan(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField(default=0)


class SerialNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='serial_numbers')
    number = models.IntegerField(default=0, verbose_name='شماره', unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان تولید')
    days_charge = models.IntegerField(default=0, verbose_name='روز های شارژ شده')

    def __str__(self):
        return f'{self.user.full_name} - {self.number}'

    class Meta:
        verbose_name = 'شماره سریال'
        verbose_name_plural = 'شماره سریال ها'


class ConfirmationCode(models.Model):
    serial_number = models.OneToOneField(SerialNumber, on_delete=models.CASCADE, verbose_name='شماره سریال', related_name='code')
    code = models.CharField(max_length=600, verbose_name='کد')
    expiry = models.BooleanField(default=False, verbose_name='انقضا')
    activation_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ فعال سازی')

    def is_active(self):
        now = timezone.now()
        days_valid = timezone.timedelta(days=self.serial_number.days_charge)
        end_date = self.activation_date + days_valid
        return self.expiry == False and now <= end_date

    def __str__(self):
        return f'{self.serial_number} - {self.code}'

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کد تایید ها'
