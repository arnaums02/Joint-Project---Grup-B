from django import forms
from django.core.exceptions import ValidationError

from .models import RoomBookings, ReservedTable, Room

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBookings
        fields = ['guestName', 'guestEmail', 'guestPhoneNumber', 'guestDNI', 'numberGuest', 'roomBooked', 'startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }

class AvailableRoomsForm(forms.Form):
    ROOM_TYPES = [
        ('standard', 'Estandar'),
        ('deluxe', 'De lujo'),
        ('lowCost', 'Economica')
    ]
    startDate = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    endDate = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'type': 'date'}))
    roomType = forms.ChoiceField(choices=ROOM_TYPES, label='Tipo de habitación')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("startDate")
        end_time = cleaned_data.get("endDate")

        if start_time is not None and end_time is not None and start_time > end_time:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de finalizacion.")

        return cleaned_data


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
