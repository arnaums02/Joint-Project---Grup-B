from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import RoomBookings
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
        roomBooking.userWhoBooked = request.user
        roomBooking.save()
        return redirect('obtainRoomBookings')
    return render(request, 'createRoomBooking.html', context)

def deleteRoomBookings(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings,id=roomBookingId)
    if request.method == 'POST':
        roomBooking.delete()
        return redirect('obtainRoomBookings')
    else:
        return HttpResponse("Bad Request: Only POST requests are allowed for this view.")