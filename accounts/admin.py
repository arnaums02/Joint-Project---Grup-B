from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser
from JointProject.models import RoomBookings, Room, Table, Shift, ReservedTable, Bill, ItemToPay, ItemPayed, CompletedPayment, RestaurantOrderedProduct, RestaurantProduct, RestaurantOrder


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RoomBookings)
admin.site.register(Room)
admin.site.register(Bill)
admin.site.register(ItemToPay)
admin.site.register(CompletedPayment)
admin.site.register(ItemPayed)
admin.site.register(RestaurantProduct)
admin.site.register(RestaurantOrder)
admin.site.register(RestaurantOrderedProduct)



@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'capacity']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['shift']


@admin.register(ReservedTable)
class ReservedTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'userWhoReserved', 'clientName', 'clientPhoneNumber', 'numberOfClients', 'reservationDate', 'tableReserved']
    list_filter = ['userWhoReserved', 'shift', 'reservationDate']
    search_fields = ['clientName', 'clientPhoneNumber']
