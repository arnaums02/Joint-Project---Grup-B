"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from JointProject.views import *
from accounts.views import signIn

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signIn, name='signIn'),
    path('accounts/login/', signIn, name='signIn'),
    path('roomStaffHomePage/', roomStaffHomePage, name='roomStaffHomePage'),
    path('obtainRoomBookings/', obtainRoomBookings, name='obtainRoomBookings'),
    path('createRoomBooking/<uuid:roomId>/<str:startDate>/<str:endDate>/', createRoomBookings, name='createRoomBookings'),
    path('deleteRoomBooking/<uuid:roomBookingId>', deleteRoomBookings, name='deleteRoomBookings'),
    #path('showAvailableRooms/', showAvailableRooms, name='showAvailableRooms'),
    path('roomBookingDetails/<uuid:roomBookingId>', roomBookingDetails, name='roomBookingDetails'),
    path('checkIn/<uuid:roomBookingId>', checkIn, name='checkIn'),
    path('checkOut/<uuid:roomBookingId>', checkOut, name='checkOut'),
    path('show_tables/', show_tables, name='show_tables'),
    path('reserve_table/<uuid:table_id>/<str:selected_date>/<str:selected_time>/', reserve_table, name='reserve_table'),
    path('consultar_reserva/<uuid:table_id>/<str:selected_date>/<str:selected_time>/', consultar_reserva,name='consultar_reserva'),
    path('getAvailableRooms/', getAvailableRooms, name='getAvailableRooms'),

    path('tableReservationHistory/', getTablesReservationHistory, name='getTablesReservationHistory'),

    path('logOut/', logOut, name='logOut'),

    path('addItemToBill/', addItemToBill, name='addItemToBill'),

    path('getCustomersBills/', getCustomersBills, name='getCustomersBills'),
    path('billDetails/<uuid:billId>', billsDetails, name='billDetails'),
    path('payBills/<uuid:billId>', payBills, name='payBills'),

    path('getCustomersCompletedPayments/', getCustomersCompletedPayments, name='getCustomersCompletedPayments'),
    path('getCustomersCompletedPaymentsDetails/<uuid:completedPaymentsId>', completedPaymentsDetails, name='completedPaymentsDetails'),

    path('addRestaurantOrder/', addRestaurantOrder, name='addRestaurantOrder'),
    path('getRestaurantOrdersHistory/', getRestaurantOrdersHistory, name='getRestaurantOrdersHistory'),
    path('addRestaurantOrderToBill/', addRestaurantOrderToBill, name='addRestaurantOrderToBill'),
    path('addRestaurantPayedOrder/', addRestaurantPayedOrder, name='addRestaurantPayedOrder'),
    path('getRestaurantOrderDetails/<uuid:orderId>', getRestaurantOrderDetails, name='getRestaurantOrderDetails'),
    path('roomsForCleaning/', roomsForCleaning, name='roomsForCleaning'),
    path('cleanedRooms/', cleanedRooms, name='cleanedRooms'),
    path('roomIsClean/<uuid:roomBookingId>', roomIsClean, name='roomIsClean'),
    path('roomToBeCleaned/<uuid:roomBookingId>', roomToBeCleaned, name='roomToBeCleaned'),
    path('tableReservationDetails/<uuid:table_id>', tableReservationDetails, name='tableReservationDetails'),
]
