from django.shortcuts import render, get_object_or_404
from .models import Cinema, Ticket, User, Movie, Purchase
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, SearchForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import os
from django.conf import settings

def index(request):
    images = []
    image_dir = [os.path.join(settings.BASE_DIR, 'static', 'images/carousel_images')]
    for directory in image_dir:
        images.append(os.listdir(directory))
    context = {'images': images}
    return render(request, 'base.html', context)


def ticket_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    tickets = set()

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            tickets = set(Movie.objects.filter(title__icontains=search))
        else:
            cities = Cinema.objects.filter(location_city__icontains=search)
            for city in cities:
                for ticket in city.ticket_set.all():
                    tickets.add(ticket.movie)

        if request.user.is_authenticated:
            search_history.append(search)
            request.session['search_history'] = search_history

    elif search_history:
        initial = dict(search=search_text,
                       search_in=search_history[-1])
        form = SearchForm(initial=initial)

    return render(request, "booking/search-results.html", {"form": form, "search_text": search_text, "tickets": tickets})

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

# views.py

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie': movie
    }
    return render(request, 'booking/movie_detail.html', context)

# def theater_detail(request, pk):
#     theater = Theater.objects.get(id=theater_id)
#     theater = get_object_or_404(Movie, pk=pk)
#     context = {
#         'theater': theater
#     }
#     return render(request, 'booking/theater_detail.html', context)

# def concert_detail(request, concert_id):
    # concert = Concert.objects.get(id=concert_id)
    # context = {
    #     'concert': concert
    # }
    # return render(request, 'booking/concert_detail.html', context)






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