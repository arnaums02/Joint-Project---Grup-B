import uuid

from accounts.models import CustomUser
from django.db import models

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Estandar'),
        ('deluxe', 'De lujo'),
        ('lowCost', 'Economica')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    booked = models.BooleanField(default=False)
    bookings = models.ManyToManyField('RoomBookings', related_name='bookings', blank=True)
    roomNumber = models.IntegerField(unique=True)
    roomType = models.CharField(max_length=30, choices=ROOM_TYPES, default='standard')


class RoomBookings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    userWhoBooked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='userWhoBooked')
    guestName = models.CharField(max_length=100)
    guestEmail = models.EmailField()
    guestPhoneNumber = models.CharField(max_length=20)
    guestDNI = models.CharField(max_length=9)
    numberGuest = models.IntegerField()
    roomBooked = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='roomBooked', default=None)
    startDate = models.DateField()
    endDate = models.DateField()



