from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Habitacio(models.Model):

class Taules(models.Model):
    name = models.CharField(max_length=100)
    HORARIS_DISPONIBLES = [
        '10:30',
        '11:00',
        '11:30',
        '12:30'
    ]

    horari = models.CharField()
    def __str__(self):
        return self.name

class ReservaTaules(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self
class ReservaHabitacio(models.Model):

    def __str__(self):
        return self