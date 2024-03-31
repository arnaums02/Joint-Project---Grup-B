# Generated by Django 5.0.3 on 2024-03-30 22:50

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('booked', models.BooleanField(default=False)),
                ('roomNumber', models.IntegerField(unique=True)),
                ('roomType', models.CharField(choices=[('standard', 'Estandar'), ('deluxe', 'De lujo'), ('lowCost', 'Economica')], default='standard', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.CharField(choices=[('12-13', '12:00 - 13:00'), ('13-14', '13:00 - 14:00'), ('14-15', '14:00 - 15:00'), ('19-20', '19:00 - 20:00'), ('20-21', '20:00 - 21:00'), ('21-22', '21:00 - 22:00')], max_length=5, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('capacity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='RoomBookings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('guestName', models.CharField(max_length=100)),
                ('guestEmail', models.EmailField(max_length=254)),
                ('guestPhoneNumber', models.CharField(max_length=20)),
                ('guestDNI', models.CharField(max_length=9)),
                ('numberGuest', models.IntegerField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('checkIn', models.BooleanField(default=False)),
                ('checkOut', models.BooleanField(default=False)),
                ('roomBooked', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='roomBooked', to='JointProject.room')),
                ('userWhoBooked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userWhoBooked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='bookings',
            field=models.ManyToManyField(blank=True, related_name='bookings', to='JointProject.roombookings'),
        ),
        migrations.CreateModel(
            name='ReservedTable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('clientName', models.CharField(max_length=20)),
                ('clientPhoneNumber', models.CharField(max_length=20)),
                ('numberOfClients', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('reservationDate', models.DateField()),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JointProject.shift')),
                ('tableReserved', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tableReserved', to='JointProject.table')),
                ('userWhoReserved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userWhoReserved', to='JointProject.table')),
            ],
            options={
                'unique_together': {('shift', 'userWhoReserved', 'reservationDate')},
            },
        ),
    ]