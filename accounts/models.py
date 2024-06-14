from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)  # Asigna el tipo proporcionado
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, user_type='admin', **extra_fields):
        if not email:
            raise ValueError('El campo correo electrónico es obligatorio')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', user_type)  # Asigna el tipo proporcionado
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('client', 'Cliente'),
        ('roomStaff', 'Personal de habitaciones'),
        ('cleaningStaff', 'Personal de limpieza'),
        ('restaurantStaff', 'Personal de restaurante'),
        ('admin', 'Administrador'),
        ('comptable', 'Comptables'),
    ]
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default='client')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def _str_(self):
        return self.email
