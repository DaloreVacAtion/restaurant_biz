from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View


class MainPageView(View):
    def get(self, request):
        return render(request, 'base.html')


class MyReservationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'booking/my_reservations.html')


class BookingView(View):
    def get(self, request):
        return render(request, 'booking/booking.html')
