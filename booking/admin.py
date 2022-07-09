from django.contrib import admin

from account.models import Check
from booking.models import Restaurant, Table, Booking


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'free_table_count', 'reserved_tables_count']
    search_fields = ['name']
    fieldsets = (
        ('Информация', {'fields': ('city', 'name', 'avg_time')}),
    )

    def free_table_count(self, obj):
        return obj.tables.filter(booking__isnull=True).count()

    def reserved_tables_count(self, obj):
        return obj.tables.filter(booking__isnull=False).count()

    free_table_count.short_description = 'Кол-во свободных столиков'
    reserved_tables_count.short_description = 'Кол-во занятых столиков'


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'capacity']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'visit_time']


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'visit_date', 'amount']
    search_fields = ['user__username', 'amount']
    search_help_text = 'Номер телефона пользователя или сумма'
