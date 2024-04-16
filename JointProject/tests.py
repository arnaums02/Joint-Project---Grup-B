from django.test import TestCase
from django.utils import timezone
from .models import Room, RoomBookings, Table, Shift, ReservedTable, Bill, ItemToPay
from accounts.models import CustomUser

class ModelTests(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email='user1@example.com', password='password1', first_name='John', last_name='Doe', user_type='client')
        self.user2 = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpassword', user_type='admin')

        self.room1 = Room.objects.create(roomNumber=101, roomType='standard')
        self.room2 = Room.objects.create(roomNumber=102, roomType='deluxe')

        self.booking1 = RoomBookings.objects.create(userWhoBooked=self.user1, guestName='Guest 1', guestEmail='guest1@example.com',
                                                    guestPhoneNumber='123456789', guestDNI='123456789A', numberGuest=2,
                                                    roomBooked=self.room1, startDate=timezone.now(), endDate=timezone.now(),
                                                    checkIn=True, checkOut=False)
        self.booking2 = RoomBookings.objects.create(userWhoBooked=self.user2, guestName='Guest 2', guestEmail='guest2@example.com',
                                                    guestPhoneNumber='987654321', guestDNI='987654321B', numberGuest=1,
                                                    roomBooked=self.room2, startDate=timezone.now(), endDate=timezone.now(),
                                                    checkIn=False, checkOut=False)

        self.table1 = Table.objects.create(tableNumber=1, capacity=4)
        self.table2 = Table.objects.create(tableNumber=2, capacity=2)
        self.shift1 = Shift.objects.create(shift='12-13')

        self.reserved_table1 = ReservedTable.objects.create(userWhoReserved=self.table1, shift=self.shift1,
                                                             clientName='Client 1', clientPhoneNumber='111222333',
                                                             numberOfClients=3, reservationDate=timezone.now(),
                                                             tableReserved=self.table1)

        self.bill1 = Bill.objects.create(customer=self.user1)
        self.item1 = ItemToPay.objects.create(name='Item 1', bill=self.bill1, details='Details for Item 1', price=10.50)

    def test_room_booking(self):
        self.assertEqual(self.booking1.userWhoBooked, self.user1)
        self.assertEqual(self.booking2.userWhoBooked, self.user2)
        self.assertTrue(self.booking1.checkIn)
        self.assertFalse(self.booking2.checkIn)

    def test_reserved_table(self):
        self.assertEqual(self.reserved_table1.userWhoReserved, self.table1)
        self.assertEqual(self.reserved_table1.shift, self.shift1)
        self.assertEqual(self.reserved_table1.clientName, 'Client 1')
        self.assertEqual(self.reserved_table1.numberOfClients, 3)

    def test_bill(self):
        self.assertEqual(self.bill1.customer, self.user1)
        self.assertEqual(self.bill1.calculateTotalPrice(), 10.50)

    def test_item_to_pay(self):
        self.assertEqual(self.item1.name, 'Item 1')
        self.assertEqual(self.item1.details, 'Details for Item 1')
        self.assertEqual(self.item1.price, 10.50)