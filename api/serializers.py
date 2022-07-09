import datetime

from django.db.models import Q
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from account.models import User
from booking.models import Restaurant, Booking, Table


class RestaurantListSerializer(serializers.ModelSerializer):
    free_tables_count = serializers.IntegerField()
    seats = serializers.IntegerField()
    avg_cost = serializers.IntegerField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'free_tables_count', 'seats', 'avg_cost', 'avg_time']


class AddBookingSerializer(serializers.ModelSerializer):
    user = PhoneNumberField()
    tables = serializers.SlugRelatedField(slug_field='id', many=True, queryset=Table.objects.all())
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ['uuid', 'tables', 'user', 'visit_time']

    def create(self, validated_data):
        username = validated_data.pop('user')
        user, _ = User.objects.get_or_create(username=username)
        booking = Booking.objects.create(
            user=user,
            visit_time=validated_data['visit_time'],
            expired_time=self.context['expired_time']
        )
        booking.save()
        for table in validated_data['tables']:
            booking.tables.add(table)
        return booking

    def validate_visit_time(self, visit_time):
        if visit_time < datetime.time(9, 00) or visit_time > datetime.time(21, 00):
            raise serializers.ValidationError("The allowed booking time between 9 and 21")
        return visit_time
