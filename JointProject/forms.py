import os

from django import forms
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from .models import RoomBookings, ReservedTable, Room, Bill, ItemToPay, RestaurantOrderedProduct, RestaurantOrder, \
    RestaurantProduct, Table, Shift


class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBookings
        fields = ['guestName', 'guestEmail', 'guestPhoneNumber', 'guestDNI', 'numberGuest']
        """widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }"""


class AvailableRoomsForm(forms.Form):
    ROOM_TYPES = [
        ('standard', 'Estandar'),
        ('deluxe', 'De lujo'),
        ('lowCost', 'Economica')
    ]
    startDate = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    endDate = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'type': 'date'}))
    roomType = forms.ChoiceField(choices=ROOM_TYPES, label='Tipo de habitación')
    capacity = forms.IntegerField(label='Numero de huespedes')

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
        ('21-22', '21:00 - 22:00'), ], widget=forms.Select())


class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservedTable
        fields = ['clientName', 'clientPhoneNumber', 'numberOfClients']


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['roomBooking']


class ItemToPayForm(forms.ModelForm):
    roomBooking = forms.ModelChoiceField(queryset=RoomBookings.objects.all(),
                                      widget=forms.Select(attrs={'class': 'customer-select'}))

    class Meta:
        model = ItemToPay
        fields = ['name', 'details', 'price']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'cols': 30}),  # Ajusta el tamaño de la caja de texto
        }


class RestaurantPayedOrderForm(forms.ModelForm):
    class Meta:
        model = RestaurantOrder
        fields = ['table', 'date', 'shift']

    def __init__(self, *args, **kwargs):
        super(RestaurantPayedOrderForm, self).__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.all()  # Obtener todas las mesas disponibles
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})  # Agregar un widget de fecha
        self.fields['shift'].queryset = Shift.objects.all()  # Obtener todos los turnos disponibles

        products = RestaurantProduct.objects.all()
        for product in products:
            self.fields[f'quantity_{product.id}'] = forms.IntegerField(label=product.name, min_value=0, required=False)

    def save(self, commit=True):
        instance = super(RestaurantPayedOrderForm, self).save(commit=False)
        if commit:
            instance.save()

        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith('quantity_') and field_value:
                product_id = field_name.replace('quantity_', '')
                quantity = field_value
                ordered_product = RestaurantOrderedProduct.objects.create(product_id=product_id, quantity=quantity,
                                                                          order=instance)

        return instance


class RestaurantOrderForm(RestaurantPayedOrderForm):
    class Meta(RestaurantPayedOrderForm.Meta):
        fields = ['roomBooking'] + RestaurantPayedOrderForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super(RestaurantOrderForm, self).__init__(*args, **kwargs)
        self.fields['roomBooking'].queryset = RoomBookings.objects.filter(checkIn=True, checkOut=False, bookingState='active')

class RoomFilterForm(forms.Form):
    FLOOR_CHOICES = [
        (1, 'Planta 1'),
        (2, 'Planta 2'),
        (3, 'Planta 3'),
        (0, 'Todas las plantas'),
    ]

    planta = forms.ChoiceField(choices=FLOOR_CHOICES, required=False,  widget=forms.Select(attrs={'class': 'rounded-select'}))


class RestaurantProductPriceForm(forms.ModelForm):
    class Meta:
        model = RestaurantProduct
        fields = ['price']



class FacturaFilterForm(forms.Form):
    year = forms.ChoiceField(label='Año')
    month = forms.ChoiceField(label='Mes', choices=[(str(i), str(i)) for i in range(1, 13)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].choices = self.get_year_choices()

    def get_year_choices(self):
        directory = 'facturas'
        if os.path.exists(directory):
            years = sorted([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])
            return [(year, year) for year in years]
        return []