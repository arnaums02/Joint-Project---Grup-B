from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your models here.
STAFF_DOMAIN = "@laspalmeras.com"


def validate_staff_email(email):
    validate_email(email)
    if not email.endswith(STAFF_DOMAIN):
        raise ValidationError('El dominio del trabajador debe ser "' + STAFF_DOMAIN + '"')


class UserRoomStaff(models.Model):
    email = models.EmailField(validators=[validate_staff_email])
    password = models.CharField(max_length=20, blank=False)
    dni = models.CharField(max_length=9)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    second_surname = models.CharField(max_length=20, blank=True)
    birthDate = models.DateField(null=True)

    def __str__(self):
        return self.email
