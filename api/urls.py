from django.urls import path

from api.views import AddBookingView

app_name = 'api'
urlpatterns = [
    path('booking/', AddBookingView.as_view(), name='booking'),
]
