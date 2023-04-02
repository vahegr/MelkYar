from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, full_name, password=None):
        """
        Creates and saves a User with the given email, phone and password.
        """
        if not phone:
            raise ValueError('لطفا شماره خود را انتخاب کنید')
        if not full_name:
            raise ValueError('داشتن نام و نام خانوادگی الزامی است')

        user = self.model(
            phone=phone,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone, password=None):
        """
        Creates and saves a superuser with the given email, phone and password.
        """
        user = self.create_user(
            phone=phone,
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
