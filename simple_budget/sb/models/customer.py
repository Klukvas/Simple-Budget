from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy

class CustomerManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(gettext_lazy('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser):
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    first_name = models.CharField(gettext_lazy('first name'), max_length=30, blank=True)
    last_name = models.CharField(gettext_lazy('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(gettext_lazy('active'), default=True)
    is_staff = models.BooleanField(gettext_lazy('staff status'), default=False)
    is_superuser = models.BooleanField(gettext_lazy('superuser status'), default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_staff
