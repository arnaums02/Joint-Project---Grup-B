from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import RoomBookings, Room, Table, Shift, ReservedTable, Bill, CompletedPayment, ItemPayed, \
    RestaurantProduct, RestaurantOrder, ItemToPay
from .forms import RoomBookingForm, MyForm, ReservationForm, AvailableRoomsForm, BillForm, ItemToPayForm, \
    RestaurantOrderForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Q


# Create your views here.


@login_required(login_url='')
def roomStaffHomePage(request):
    return render(request, 'roomStaffHomePage.html')


@login_required(login_url='')
def obtainRoomBookings(request):
    roomBookings = RoomBookings.objects.all()
    context = {
        'roomBookings': roomBookings
    }
    return render(request, 'obtainRoomBookings.html', context)


@login_required(login_url='')
def createRoomBookings(request, roomId, startDate, endDate):
    form = RoomBookingForm(request.POST)
    context = {
        'form': form
    }
    if form.is_valid():
        roomBooking = form.save(commit=False)
        """
        if roomBooking.roomBooked.booked == False:
            roomBooking.userWhoBooked = request.user
            roomBooking.roomBooked.booked = True
            roomBooking.save()
            return redirect('obtainRoomBookings')
        else:
            return HttpResponse("Room already booked")"""
        roomBooking.userWhoBooked = request.user
        roomBooking.roomBooked = Room.objects.get(id=roomId)
        roomBooking.startDate = startDate
        roomBooking.endDate = endDate
        roomBooking.save()
        return redirect('obtainRoomBookings')
    return render(request, 'createRoomBooking.html', context)


@login_required(login_url='')
def deleteRoomBookings(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)
    if request.method == 'POST':
        roomBooking.delete()
        return redirect('obtainRoomBookings')
    else:
        return HttpResponse("Bad Request: Only POST requests are allowed for this view.")


"""def showAvailableRooms(request):
    rooms = Room.objects.filter(booked=False)
    context = {
        'rooms' : rooms
    }
    return render(request, 'availableRoomBookings.html', context)"""

"""def getAvailableRooms(request):
    if request.method == 'POST':    
        form = AvailableRoomsForm(request.POST)
        if form.is_valid():
            room = """


@login_required(login_url='')
def getAvailableRooms(request):
    if request.method == 'POST':
        form = AvailableRoomsForm(request.POST)
        if form.is_valid():
            startTime = form.cleaned_data['startDate']
            endTime = form.cleaned_data['endDate']
            roomType = form.cleaned_data['roomType']

            availableRooms = checkAvailableRooms(startTime, endTime, roomType)

            context = {
                'rooms': availableRooms,
                'startDate': startTime,
                'endDate': endTime
            }
            return render(request, 'availableRoomBookings.html', context)
    else:
        form = AvailableRoomsForm()
    context = {
        'form': form
    }
    return render(request, 'getAvailableRooms.html', context)


def checkAvailableRooms(startTime, endTime, roomType):
    colidingRoomBookings = RoomBookings.objects.filter(Q(startDate__lte=endTime, endDate__gte=startTime) |
                                                       Q(startDate__gte=startTime, startDate__lte=endTime) |
                                                       Q(endDate__gte=startTime, endDate__lte=endTime))

    filteredTypeRooms = Room.objects.filter(roomType=roomType)
    colidingRoomBookings.filter(roomBooked__in=filteredTypeRooms)
    availableRooms = filteredTypeRooms.exclude(pk__in=colidingRoomBookings.values_list('roomBooked__pk', flat=True))

    return availableRooms


@login_required(login_url='')
def roomBookingDetails(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)
    context = {
        'roomBooking': roomBooking
    }
    return render(request, 'roomBookingDetails.html', context)


@login_required(login_url='')
def checkIn(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)
    context = {
        'roomBooking': roomBooking
    }
    roomBooking.checkIn = True
    roomBooking.save()
    return render(request, 'roomBookingDetails.html', context)


@login_required(login_url='')
def checkOut(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)
    context = {
        'roomBooking': roomBooking
    }
    if roomBooking.checkIn:
        roomBooking.checkOut = True
        roomBooking.toClean = True
        roomBooking.save()
    return render(request, 'roomBookingDetails.html', context)


@login_required(login_url='')
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
                if shift_wanted is None:
                    messages.error(request, "No hay turnos disponibles actualmente.")

                else:
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


# @login_required(login_url='')
def get_shift_with_time(time):  # The format of the param(time) is HH-HH
    try:
        return Shift.objects.get(shift=time)
    except Shift.DoesNotExist:
        return None


# @login_required(login_url='')
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
            'num': table.tableNumber,
            'capacity': table.capacity,
        }
        if table.id in reserved_table_ids:
            reserved_tables.append(table_info)
        else:
            available_tables.append(table_info)

    return available_tables, reserved_tables


@login_required(login_url='')
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
                # creamos la reserva
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
        'num': table.tableNumber,
        'capacity': table.capacity,
        'selected_date': selected_date,
        'selected_time': selected_time
    }
    return render(request, 'reserve_table.html', context)


@login_required(login_url='')
def consultar_reserva(request, table_id, selected_date, selected_time):
    fecha_seleccionada = datetime.strptime(selected_date, "%d-%m-%Y").date()

    hour = selected_time.split(":")[0]
    start_hour = f"{hour}-{int(hour) + 1:02d}"  # Hora con formato "HH-HH"
    shift_wanted = get_shift_with_time(start_hour)

    try:
        reserva = ReservedTable.objects.get(tableReserved_id=table_id, reservationDate=fecha_seleccionada,
                                            shift=shift_wanted)
    except ReservedTable.DoesNotExist:
        return HttpResponse("No se encontró ninguna reserva para esta mesa en esa hora.")

    context = {
        'reserva': reserva,
        'selected_date': selected_date,
        'selected_time': selected_time,
    }
    return render(request, 'info_reserve.html', context)



@login_required(login_url='')
def tableReservationDetails(request, table_id):
    reserva = get_object_or_404(ReservedTable, id=table_id)
    context = {
        'reserva': reserva
    }
    return render(request, 'tableReservationDetails.html', context)

@login_required(login_url='')
def getTablesReservationHistory(request):
    tablesReservations = ReservedTable.objects.all()
    context = {
        'tablesReservations': tablesReservations
    }
    return render(request, 'tableReservationHistory.html', context)


def logOut(request):
    logout(request)
    return redirect('signIn')


@login_required(login_url='')
def addItemToBill(request):
    if request.method == 'POST':
        form = ItemToPayForm(request.POST)
        itemToPay = form.save(commit=False)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            try:
                bill = Bill.objects.get(customer=customer)
            except Bill.DoesNotExist:
                bill = Bill.objects.create(customer=customer)
            itemToPay.bill = bill
            itemToPay.save()
            return redirect('getCustomersBills')
    else:
        form = ItemToPayForm()
    context = {
        'form': form
    }
    return render(request, 'addItemToBill.html', context)


@login_required(login_url='')
def getCustomersBills(request):
    bills = Bill.objects.all()
    context = {
        'bills': bills
    }
    return render(request, 'getCustomersBills.html', context)


@login_required(login_url='')
def billsDetails(request, billId):
    bill = get_object_or_404(Bill, id=billId)
    totalPrice = bill.calculateTotalPrice()
    context = {
        'bill': bill,
        'totalPrice': totalPrice
    }
    return render(request, 'billDetails.html', context)


@login_required(login_url='')
def payBills(request, billId):
    bill = get_object_or_404(Bill, id=billId)
    items = bill.items.all()
    customer = bill.customer

    try:
        completedPayment = CompletedPayment.objects.get(customer=customer)
    except CompletedPayment.DoesNotExist:
        completedPayment = CompletedPayment.objects.create(customer=customer)

    for item in items:
        ItemPayed.objects.create(
            name=item.name,
            price=item.price,
            details=item.details,
            completedPayment=completedPayment
        )

    items.delete()
    return redirect('getCustomersBills')


@login_required(login_url='')
def getCustomersCompletedPayments(request):
    completedPayments = CompletedPayment.objects.all()
    context = {
        'completedPayments': completedPayments
    }
    return render(request, 'getCustomersCompletedPayments.html', context)


@login_required(login_url='')
def completedPaymentsDetails(request, completedPaymentsId):
    completedPayment = get_object_or_404(CompletedPayment, id=completedPaymentsId)
    totalPayed = completedPayment.calculateTotalPayed()
    context = {
        'completedPayment': completedPayment,
        'totalPayed': totalPayed
    }
    return render(request, 'completedPaymentsDetails.html', context)


@login_required(login_url='')
def addRestaurantOrder(request):
    return render(request, 'addRestaurantOrder.html')


@login_required(login_url='')
def getRestaurantOrdersHistory(request):
    context = {
        'restaurantOrders': RestaurantOrder.objects.all()
    }
    return render(request, 'getRestaurantOrdersHistory.html', context)


@login_required(login_url='')
def addRestaurantOrderToBill(request):
    if request.method == 'POST':
        form = RestaurantOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            customer = form.cleaned_data['customer']
            try:
                bill = Bill.objects.get(customer=customer)
            except Bill.DoesNotExist:
                bill = Bill.objects.create(customer=customer)
            ItemToPay.objects.create(name="Restaurante", bill=bill,
                                     details="Fecha:" + form.cleaned_data['date'].strftime(""),
                                     price=order.calculateTotalOrder())
            return redirect('getRestaurantOrdersHistory')
    else:
        form = RestaurantOrderForm()
        context = {
            'form': form
        }
    return render(request, 'addRestaurantOrderToBill.html', context)


@login_required(login_url='')
def addRestaurantPayedOrder(request):
    if request.method == 'POST':
        form = RestaurantOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('getRestaurantOrdersHistory')
    else:
        form = RestaurantOrderForm()
        form.fields.pop('customer')
        context = {
            'form': form
        }
    return render(request, 'addRestaurantPayedOrder.html', context)


@login_required(login_url='')
def getRestaurantOrderDetails(request, orderId):
    order = get_object_or_404(RestaurantOrder, id=orderId)
    totalPrice = order.calculateTotalOrder()
    context = {
        'order': order,
        'totalPrice': totalPrice
    }
    return render(request, 'getRestaurantOrderDetails.html', context)


@login_required(login_url='')
def roomsForCleaning(request):
    roomBookings = RoomBookings.objects.all()
    context = {
        'roomBookings': roomBookings
    }
    return render(request, 'roomsForCleaning.html', context)


@login_required(login_url='')
def cleanedRooms(request):
    roomBookings = RoomBookings.objects.all()
    context = {
        'roomBookings': roomBookings
    }
    return render(request, 'cleanedRooms.html', context)


@login_required(login_url='')
def roomIsClean(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)

    if roomBooking.checkIn:
        roomBooking.toClean = False
        roomBooking.cleaned = True
        roomBooking.save()
    return redirect('roomsForCleaning')


@login_required(login_url='')
def roomToBeCleaned(request, roomBookingId):
    roomBooking = get_object_or_404(RoomBookings, id=roomBookingId)

    if roomBooking.checkIn:
        roomBooking.toClean = True
        roomBooking.cleaned = False
        roomBooking.save()
    return redirect('cleanedRooms')
