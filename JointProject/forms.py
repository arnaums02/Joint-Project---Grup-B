from django import forms
from .models import RoomBookings

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBookings
        fields = ['guestName', 'guestEmail', 'guestPhoneNumber', 'guestDNI', 'numberGuest', 'roomBooked', 'startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(),
            'endDate': forms.DateInput(),
        }
