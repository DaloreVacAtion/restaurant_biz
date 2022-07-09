from django.urls import path

from booking.views import MyReservationView, BookingView

app_name = 'booking'
urlpatterns = [
    path('my_reservation/', MyReservationView.as_view(), name='my_reservation'),
    path('', BookingView.as_view(), name='booking'),
]
