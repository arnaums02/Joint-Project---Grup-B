from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import RoomBookings, Room
from .forms import RoomBookingForm


# Create your views here.


def roomStaffHomePage(request):
    return render(request, 'roomStaffHomePage.html')

def obtainRoomBookings(request):
    roomBookings = RoomBookings.objects.all()
    context = {
        'roomBookings' : roomBookings
    }
    return render(request, 'obtainRoomBookings.html', context)

def createRoomBookings(request):
    form = RoomBookingForm(request.POST)
    context = {
        'form' : form
    }
    if form.is_valid():
        roomBooking = form.save(commit=False)
        if roomBooking.roomBooked.booked == False:
            roomBooking.userWhoBooked = request.user
            roomBooking.roomBooked.booked = True
            roomBooking.save()
            return redirect('obtainRoomBookings')
        else:
            return HttpResponse("Room already booked")
    return render(request, 'createRoomBooking.html', context)

def deleteRoomBookings(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings,id=roomBookingId)
    if request.method == 'POST':
        roomBooking.delete()
        return redirect('obtainRoomBookings')
    else:
        return HttpResponse("Bad Request: Only POST requests are allowed for this view.")

def availableRooms(request):
    rooms = Room.objects.filter(booked=False)
    context = {
        'rooms' : rooms
    }
    return render(request, 'availableRoomBookings.html', context)

def roomBookingDetails(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings,id=roomBookingId)
    context = {
        'roomBooking' : roomBooking
    }
    return render(request, 'roomBookingDetails.html', context)

def checkIn(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings,id=roomBookingId)
    context={
        'roomBooking' : roomBooking
    }
    roomBooking.checkIn = True
    roomBooking.save()
    return render(request, 'roomBookingDetails.html', context)


def checkOut(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings,id=roomBookingId)
    context={
        'roomBooking' : roomBooking
    }
    roomBooking.checkOut = True
    roomBooking.save()
    return render(request, 'roomBookingDetails.html', context)