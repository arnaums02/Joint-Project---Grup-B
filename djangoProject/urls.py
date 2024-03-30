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
from JointProject.views import roomStaffHomePage, obtainRoomBookings, createRoomBookings, deleteRoomBookings, availableRooms, roomBookingDetails, checkIn, checkOut
from accounts.views import signIn

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signIn, name='signIn'),
    path('roomStaffHomePage/', roomStaffHomePage, name='roomStaffHomePage'),
    path('obtainRoomBookings/', obtainRoomBookings, name='obtainRoomBookings'),
    path('createRoomBooking/', createRoomBookings, name='createRoomBookings'),
    path('deleteRoomBooking/<uuid:roomBookingId>', deleteRoomBookings, name='deleteRoomBookings'),
    path('availableRooms/', availableRooms, name='availableRooms'),
    path('roomBookingDetails/<uuid:roomBookingId>', roomBookingDetails, name='roomBookingDetails'),
    path('checkIn/<uuid:roomBookingId>', checkIn, name='checkIn'),
    path('checkOut/<uuid:roomBookingId>', checkOut, name='checkOut'),
]
