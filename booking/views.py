from django.shortcuts import render, get_object_or_404
from .models import Movie, Theater, Seat, Booking, User
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages



def index(request):
    return render(request, 'booking/theater_detail.html')

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'booking/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('booking:movie_list')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'booking/login.html', {'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('booking:movie_list')

# def movie_detail(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     theaters = Theater.objects.filter(movie=movie)
#     context = {'movie': movie, 'theaters': theaters}
#     return render(request, 'booking/movie_detail.html', context)
#
# def theater_detail(request, theater_id):
#     theater = get_object_or_404(Theater, pk=theater_id)
#     seats = Seat.objects.filter(theater=theater)
#     context = {'theater': theater, 'seats': seats}
#     return render(request, 'booking/theater_detail.html', context)
#
# def booking_confirmation(request, movie_id, theater_id, seat_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     theater = get_object_or_404(Theater, pk=theater_id)
#     seat = get_object_or_404(Seat, pk=seat_id)
#     user = request.user
#     booking = Booking.objects.create(user=user, movie=movie, theater=theater, seat=seat)
#     context = {'booking': booking}
#     return render(request, 'booking/', context)






def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'booking/register.html', { 'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('booking:movie_list')
        else:
            return render(request, 'booking/register.html', {'form': form})