import uuid

from accounts.models import CustomUser
from django.db import models

# Create your models here.

class RoomBookings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    userWhoBooked = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    guestName = models.CharField(max_length=100)
    guestEmail = models.EmailField()
    guestPhoneNumber = models.CharField(max_length=20)
    guestDNI = models.CharField(max_length=9)
    numberGuest = models.IntegerField()
    room = models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()

