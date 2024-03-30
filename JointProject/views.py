from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import RoomBookings, Room, Table, Shift, ReservedTable
from .forms import RoomBookingForm, MyForm, ReservationForm
from django.contrib import messages
from datetime import datetime
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


def show_tables(request):
    available_tables = None
    reserved_tables = None
    start_hour = None
    date_format = None

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['my_date_field']
            selected_time = form.cleaned_data['my_time_field']

            if selected_date and selected_time:  # Verificar si ambos campos están completos
                shift_wanted = get_shift_with_time(selected_time)

                # Obtener mesas disponibles y reservadas usando la función get_available_and reserved_tables.
                available_tables, reserved_tables = get_available_and_reserved_tables(shift_wanted, selected_date)

                start_hour = selected_time.split("-")[0] + ":00"
                date_format = selected_date.strftime("%d-%m-%Y")
        else:
            messages.error(request, "Por favor assegurate de rellenar tanto fecha como hora para buscar.")
            return redirect('show_tables')
    else:
        form = MyForm()

    context = {
        'form': form,
        'selected_date': date_format,
        'selected_time': start_hour,
        'available_tables': available_tables,
        'reserved_tables': reserved_tables,
    }

    return render(request, 'show_tables.html', context)


def get_shift_with_time(time): #The format of the param(time) is HH-HH
    try:
        return Shift.objects.get(shift=time)
    except Shift.DoesNotExist:
        raise Http404("El turno seleccionado no existe.")


def get_available_and_reserved_tables(shift, selected_date):
    """
        Retrieves available and reserved tables for a specific shift and date.

        :param shift: The Shift object corresponding to the selected shift.
        :param selected_date: The selected date.
        :return: A tuple containing two lists, the first one with information of available tables and the second one with
               information of reserved tables.
    """
    reserved_tables_queryset = ReservedTable.objects.filter(
        reservationDate=selected_date,
        shift=shift
    )
    all_tables = Table.objects.all()

    reserved_table_ids = set(reserved.tableReserved_id for reserved in reserved_tables_queryset)

    available_tables = []
    reserved_tables = []
    for table in all_tables:
        table_info = {
            'id': table.id,
            'capacity': table.capacity,
        }
        if table.id in reserved_table_ids:
            reserved_tables.append(table_info)
        else:
            available_tables.append(table_info)

    return available_tables, reserved_tables



def reserve_table(request, table_id, selected_date, selected_time):
    try:
        table = Table.objects.get(pk=table_id)
        hour = selected_time.split(":")[0]
        start_hour = f"{hour}-{int(hour) + 1:02d}"
        shift_wanted = Shift.objects.get(shift=start_hour)
    except (Table.DoesNotExist, Shift.DoesNotExist):
        raise Http404("La mesa o el turno seleccionado no existen.")

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                #creamos la reserva
                reservation = ReservedTable.objects.create(
                    shift=shift_wanted,
                    userWhoReserved=table,
                    tableReserved=table,
                    reservationDate=datetime.strptime(selected_date, "%d-%m-%Y").date(),
                    **form.cleaned_data
                )
                reservation.save()
                messages.success(request, '¡Reserva realizada con éxito!')
                return redirect('show_tables')
            except Exception as e:
                messages.error(request, f'Error al realizar la reserva: {str(e)}')
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'table_id': table_id,
        'capacity': table.capacity,
        'selected_date': selected_date,
        'selected_time': selected_time
    }
    return render(request, 'reserve_table.html', context)


def consultar_reserva(request, table_id, selected_date, selected_time):
    fecha_seleccionada = datetime.strptime(selected_date, "%d-%m-%Y").date()

    hour = selected_time.split(":")[0]
    start_hour = f"{hour}-{int(hour) + 1:02d}"  #Hora con formato "HH-HH"
    shift_wanted = get_shift_with_time(start_hour)

    try:
        reserva = ReservedTable.objects.get(tableReserved_id=table_id, reservationDate=fecha_seleccionada, shift=shift_wanted)
    except ReservedTable.DoesNotExist:
        return HttpResponse("No se encontró ninguna reserva para esta mesa en esa hora.")

    context = {
        'reserva': reserva,
        'selected_date': selected_date,
        'selected_time': selected_time,
    }
    return render(request, 'info_reserve.html', context)



