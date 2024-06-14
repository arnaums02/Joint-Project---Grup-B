import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from accounts.models import CustomUser
from .models import Room, RoomBookings, Table, Shift, ReservedTable, Bill, ItemToPay


class ModelTests(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email='user1@example.com', password='password1', first_name='John',
                                                    last_name='Doe', user_type='client')
        self.user2 = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpassword',
                                                         user_type='admin')

        self.room1 = Room.objects.create(roomNumber=101, roomType='standard')
        self.room2 = Room.objects.create(roomNumber=102, roomType='deluxe')

        self.booking1 = RoomBookings.objects.create(userWhoBooked=self.user1, guestName='Guest Enero',
                                                    guestEmail='guest1@example.com',
                                                    guestPhoneNumber='123456789', guestDNI='123456789A', numberGuest=2,
                                                    roomBooked=self.room1, startDate=timezone.now(),
                                                    endDate=timezone.now(),
                                                    checkIn=True, checkOut=False)
        self.booking2 = RoomBookings.objects.create(userWhoBooked=self.user2, guestName='Guest 2',
                                                    guestEmail='guest2@example.com',
                                                    guestPhoneNumber='987654321', guestDNI='987654321B', numberGuest=1,
                                                    roomBooked=self.room2, startDate=timezone.now(),
                                                    endDate=timezone.now(),
                                                    checkIn=False, checkOut=False)

        self.table1 = Table.objects.create(tableNumber=1, capacity=4)
        self.table2 = Table.objects.create(tableNumber=2, capacity=2)
        self.shift1 = Shift.objects.create(shift='12-13')

        self.reserved_table1 = ReservedTable.objects.create(userWhoReserved=self.table1, shift=self.shift1,
                                                            clientName='Client Enero', clientPhoneNumber='111222333',
                                                            numberOfClients=3, reservationDate=timezone.now(),
                                                            tableReserved=self.table1)

        self.bill1 = Bill.objects.create(customer=self.user1)
        self.item1 = ItemToPay.objects.create(name='Item Enero', bill=self.bill1, details='Details for Item Enero', price=10.50)

    def test_room_booking(self):
        self.assertEqual(self.booking1.userWhoBooked, self.user1)
        self.assertEqual(self.booking2.userWhoBooked, self.user2)
        self.assertTrue(self.booking1.checkIn)
        self.assertFalse(self.booking2.checkIn)

    def test_reserved_table(self):
        self.assertEqual(self.reserved_table1.userWhoReserved, self.table1)
        self.assertEqual(self.reserved_table1.shift, self.shift1)
        self.assertEqual(self.reserved_table1.clientName, 'Client Enero')
        self.assertEqual(self.reserved_table1.numberOfClients, 3)

    def test_bill(self):
        self.assertEqual(self.bill1.customer, self.user1)
        self.assertEqual(self.bill1.calculateTotalPrice(), 10.50)

    def test_item_to_pay(self):
        self.assertEqual(self.item1.name, 'Item Enero')
        self.assertEqual(self.item1.details, 'Details for Item Enero')
        self.assertEqual(self.item1.price, 10.50)


class LoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(
            user_type='roomStaff',
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.live_server_url)

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field = self.selenium.find_element(By.NAME, "password")
        email_field.send_keys('test@example.com')
        password_field.send_keys('password')

        login_button = self.selenium.find_element(By.XPATH, "//button[@type='Submit']")
        login_button.click()

        self.assertEqual(self.selenium.current_url, self.live_server_url + '/homePage/')


class CleanRoomsTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        room = Room.objects.create(roomNumber=101, roomType='standard', roomFloor=1)
        cls.user = CustomUser.objects.create_user(
            user_type='cleaningStaff',
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User')

        cls.reservation = RoomBookings.objects.create(
            userWhoBooked=CustomUser.objects.first(),
            guestName='Test client',
            guestEmail='test@example.com',
            guestPhoneNumber='123456789',
            guestDNI='123456789A',
            numberGuest=2,
            roomBooked=room,
            startDate=timezone.now(),
            endDate=timezone.now(),
            checkIn=True,
            checkOut=True,
            toClean=True,
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        cls.selenium = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_clean_room(self):
        roomBooking = RoomBookings.objects.get(guestName='Test client')

        self.assertEqual(roomBooking.toClean, True)
        self.assertEqual(roomBooking.cleaned, False)
        self.selenium.get(self.live_server_url)

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field = self.selenium.find_element(By.NAME, "password")
        email_field.send_keys('test@example.com')
        password_field.send_keys('password')

        login_button = self.selenium.find_element(By.XPATH, "//button[@type='Submit']")
        login_button.click()

        self.selenium.get(self.live_server_url + "/roomsForCleaning/")

        self.assertEqual(self.selenium.current_url, self.live_server_url + "/roomsForCleaning/")

        confirm_button = self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Confirmar limpieza')]")
        confirm_button.click()

        roomBooking = RoomBookings.objects.get(guestName='Test client')

        self.assertEqual(roomBooking.toClean, False)

        self.assertEqual(roomBooking.cleaned, True)




