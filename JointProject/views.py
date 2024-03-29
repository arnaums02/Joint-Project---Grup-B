from django.shortcuts import render, redirect
from .models import RoomBookings


# Create your views here.


def roomStaffHomePage(request):
    return render(request, 'roomStaffHomePage.html')

def obtainRoomBookings(request):
    roomBookings = RoomBookings.objects.all()
    context = {
        'roomBookings' : roomBookings
    }
    return render(request, 'obtainRoomBookings.html', context)
