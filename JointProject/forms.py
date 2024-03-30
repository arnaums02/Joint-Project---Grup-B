from django import forms
from .models import RoomBookings, ReservedTable

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBookings
        fields = ['guestName', 'guestEmail', 'guestPhoneNumber', 'guestDNI', 'numberGuest', 'roomBooked', 'startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(),
            'endDate': forms.DateInput(),
        }


class MyForm(forms.Form):
    my_date_field = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    my_time_field = forms.ChoiceField(choices=[
                                        ('12-13', '12:00 - 13:00'),
                                        ('13-14', '13:00 - 14:00'),
                                        ('14-15', '14:00 - 15:00'),
                                        ('19-20', '19:00 - 20:00'),
                                        ('20-21', '20:00 - 21:00'),
                                        ('21-22', '21:00 - 22:00'),], widget=forms.Select())

class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservedTable
        fields = ['clientName', 'clientPhoneNumber', 'numberOfClients']
