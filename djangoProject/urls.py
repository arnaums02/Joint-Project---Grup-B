"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    Enero. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    Enero. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    Enero. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path
from JointProject.views import *
from accounts.views import signIn, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', homePage, name='homePage'),
    path('accounts/login/', signIn, name='signIn'),
    path('profilePage/', profilePage, name='profilePage'),
    path('obtainRoomBookings/<str:bookingState>', obtainRoomBookings, name='obtainRoomBookings'),
    path('obtainRoomBookings/', obtainRoomBookings, {'bookingState': 'active'}, name='obtainRoomBookings'),
    path('cancelRoomBoq'
         'oking/<uuid:roomBookingId>', cancelRoomBooking, name='cancelRoomBooking'),
    path('activateRoomBooking/<uuid:roomBookingId>', activateRoomBooking, name='activateRoomBooking'),
    path('createRoomBooking/<uuid:roomId>/<str:startDate>/<str:endDate>/', createRoomBookings,
         name='createRoomBookings'),
    path('deleteRoomBooking/<uuid:roomBookingId>', deleteRoomBookings, name='deleteRoomBookings'),
    # path('showAvailableRooms/', showAvailableRooms, name='showAvailableRooms'),
    path('roomBookingDetails/<uuid:roomBookingId>', roomBookingDetails, name='roomBookingDetails'),
    path('checkIn/<uuid:roomBookingId>', checkIn, name='checkIn'),
    path('checkOut/<uuid:roomBookingId>', checkOut, name='checkOut'),
    path('show_tables/', show_tables, name='show_tables'),
    path('reserve_table/<uuid:table_id>/<str:selected_date>/<str:selected_time>/', reserve_table, name='reserve_table'),
    path('consultar_reserva/<uuid:table_id>/<str:selected_date>/<str:selected_time>/', consultar_reserva,
         name='consultar_reserva'),
    path('getAvailableRooms/', getAvailableRooms, name='getAvailableRooms'),

    path('tableReservationHistory/', getTablesReservationHistory, name='getTablesReservationHistory'),

    path('logOut/', logOut, name='logOut'),

    path('addItemToBill/', addItemToBill, name='addItemToBill'),

    path('getCustomersBills/', getCustomersBills, name='getCustomersBills'),
    path('billDetails/<uuid:billId>', billsDetails, name='billDetails'),
    path('payBills/<uuid:billId>', payBills, name='payBills'),

    path('getCustomersCompletedPayments/', getCustomersCompletedPayments, name='getCustomersCompletedPayments'),
    path('getCustomersCompletedPaymentsDetails/<uuid:completedPaymentsId>', completedPaymentsDetails,
         name='completedPaymentsDetails'),

    path('addRestaurantOrder/', addRestaurantOrder, name='addRestaurantOrder'),
    path('getRestaurantOrdersHistory/', getRestaurantOrdersHistory, name='getRestaurantOrdersHistory'),
    path('addRestaurantOrderToBill/', addRestaurantOrderToBill, name='addRestaurantOrderToBill'),
    path('addRestaurantPayedOrder/', addRestaurantPayedOrder, name='addRestaurantPayedOrder'),
    path('getRestaurantOrderDetails/<uuid:orderId>', getRestaurantOrderDetails, name='getRestaurantOrderDetails'),
    path('roomsForCleaning/P<str:floor>', roomsForCleaning, name='roomsForCleaning'),
    path('roomsForCleaning/', roomsForCleaning, {'floor': 'all'}, name='roomsForCleaning'),
    path('cleanedRooms/P<int:floor>', cleanedRooms, name='cleanedRooms'),
    path('cleanedRooms/', cleanedRooms, {'floor': 'all'}, name='cleanedRooms'),
    path('roomIsClean/<uuid:roomBookingId>/<int:floor>', roomIsClean, name='roomIsClean'),

    path('roomToBeCleaned/', roomToBeCleaned, name='roomToBeCleaned'),

    path('tableReservationDetails/<uuid:table_id>', tableReservationDetails, name='tableReservationDetails'),

    path('about_us/', about_us, name='about_us'),


    path('room-bookings/cleaning/', room_booking_cleaning_view, name='room_bookings_cleaning'),
    path('room-bookings/<uuid:booking_id>/mark-as-cleaned/', mark_as_cleaned, name='mark_as_cleaned'),

    path('room-bookings/clean/', room_bookings_clean_view, name='room_bookings_clean'),
    path('room-bookings/<uuid:booking_id>/mark-as-dirty/', mark_as_dirty, name='mark_as_dirty'),


    path('manage-prices/', manage_prices, name='manage_prices'),
    path('getHotelBills/', getHotelBills, name='getHotelBills'),

    path('showPDF/<str:year>/<str:month>/<str:day>/<str:pdf>', pdf_view, name='pdf_view')
]

