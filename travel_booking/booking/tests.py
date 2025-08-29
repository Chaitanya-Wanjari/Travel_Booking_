
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TravelOption, Booking

class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')
        self.travel = TravelOption.objects.create(
            type='Bus', source='A', destination='B',
            date_time=timezone.now() + timezone.timedelta(days=1),
            price=500, available_seats=10
        )

    def test_create_booking_and_seat_decrement(self):
        self.client.login(username='alice', password='pass12345')
        resp = self.client.post(f'/travels/{self.travel.pk}/book/', { 'number_of_seats': 3 })
        self.assertEqual(resp.status_code, 302)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 7)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_booking_refunds_seats(self):
        self.client.login(username='alice', password='pass12345')
        self.client.post(f'/travels/{self.travel.pk}/book/', { 'number_of_seats': 4 })
        booking = Booking.objects.first()
        resp = self.client.post(f'/bookings/{booking.pk}/cancel/')
        self.assertEqual(resp.status_code, 302)
        self.travel.refresh_from_db(); booking.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 10)
        self.assertEqual(booking.status, 'Cancelled')
