
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from .models import TravelOption, Booking
from .forms import SignUpForm, ProfileForm, BookingForm, FilterForm
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created.')
            return redirect('list_travel_options')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def list_travel_options(request):
    form = FilterForm(request.GET or None)
    qs = TravelOption.objects.all().order_by('date_time')
    # filters
    if form.is_valid():
        t = form.cleaned_data.get('type')
        src = form.cleaned_data.get('source')
        dst = form.cleaned_data.get('destination')
        date = form.cleaned_data.get('date')
        if t:
            qs = qs.filter(type=t)
        if src:
            qs = qs.filter(source__icontains=src)
        if dst:
            qs = qs.filter(destination__icontains=dst)
        if date:
            qs = qs.filter(date_time__date=date)

    # search suggestions endpoint handled via JS calling /travels/suggest/
    paginator = Paginator(qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list_travel_options.html', {'page_obj': page_obj, 'form': form})

@login_required
def travel_suggestions(request):
    q = request.GET.get('q','')
    suggestions = []
    if q:
        qs = TravelOption.objects.filter(destination__istartswith=q).values_list('destination', flat=True).distinct()[:6]
        suggestions = list(qs)
    return JsonResponse({'suggestions': suggestions})

@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, pk=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            if seats < 1:
                messages.error(request, 'Seats must be at least 1')
                return redirect('book_travel', travel_id=travel_id)
            with transaction.atomic():
                travel_locked = TravelOption.objects.select_for_update().get(pk=travel_id)
                if travel_locked.available_seats < seats:
                    messages.error(request, 'Not enough seats available')
                    return redirect('book_travel', travel_id=travel_id)
                travel_locked.available_seats -= seats
                travel_locked.save()
                booking = Booking.objects.create(
                    user=request.user,
                    travel_option=travel_locked,
                    number_of_seats=seats,
                    total_price=seats * travel_locked.price
                )
            messages.success(request, f'Booked {seats} seat(s). Booking ID: {booking.booking_id}')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'travel': travel, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('travel_option').order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST' and booking.status == 'Confirmed':
        with transaction.atomic():
            travel_locked = TravelOption.objects.select_for_update().get(pk=booking.travel_option_id)
            travel_locked.available_seats += booking.number_of_seats
            travel_locked.save()
            booking.status = 'Cancelled'
            booking.save(update_fields=['status'])
        messages.success(request, 'Booking cancelled and seats refunded')
    return redirect('my_bookings')
