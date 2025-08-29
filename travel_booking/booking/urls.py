
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),

    path('travels/', views.list_travel_options, name='list_travel_options'),
    path('travels/suggest/', views.travel_suggestions, name='travel_suggestions'),
    path('travels/<int:travel_id>/book/', views.book_travel, name='book_travel'),

    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
