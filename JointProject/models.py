import uuid

from django.core.validators import MinValueValidator
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
    #booked = models.BooleanField(default=False)
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
    checkIn = models.BooleanField(default=False)
    checkOut = models.BooleanField(default=False)

    toClean = models.BooleanField(default=False)
    cleaned = models.BooleanField(default=False)


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    tableNumber = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.tableNumber)


class Shift(models.Model):
    SHIFT_CHOICES = (
        ('12-13', '12:00 - 13:00'),
        ('13-14', '13:00 - 14:00'),
        ('14-15', '14:00 - 15:00'),
        ('19-20', '19:00 - 20:00'),
        ('20-21', '20:00 - 21:00'),
        ('21-22', '21:00 - 22:00'),
    )

    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES, unique=True)
    def __str__(self):
        return self.shift


class ReservedTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    userWhoReserved = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='userWhoReserved') # cambiar table per # CustomUser
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=20)
    clientPhoneNumber = models.CharField(max_length=20)
    numberOfClients = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    reservationDate = models.DateField()
    tableReserved = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='tableReserved', default=None)

    class Meta:
        unique_together = ('shift', 'userWhoReserved', 'reservationDate') # Evitar duplicaciones de reservas

class Bill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer')

    def calculateTotalPrice(self):
        totalPrice = sum(item.price for item in self.items.all())
        return totalPrice

class ItemToPay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class CompletedPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customerWhoPayed')

    def calculateTotalPayed(self):
        totalPrice = sum(item.price for item in self.items.all())
        return totalPrice


class ItemPayed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    completedPayment = models.ForeignKey(CompletedPayment, on_delete=models.CASCADE, related_name='items')
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class RestaurantProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class RestaurantOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(RestaurantProduct, through="RestaurantOrderedProduct")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)


    def calculateTotalOrder(self):
        totalPrice = 0
        for orderedProduct in RestaurantOrderedProduct.objects.filter(order=self):
            totalPrice += orderedProduct.quantity * orderedProduct.product.price
        return totalPrice

class RestaurantOrderedProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(RestaurantProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE)



