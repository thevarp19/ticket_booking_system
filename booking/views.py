from django.shortcuts import render, get_object_or_404
from .models import Place, Event, Ticket, User, Purchase
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, SearchForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import os
from django.conf import settings

def index(request):
    events = Event.objects.all()
    images = []
    image_dir = [os.path.join(settings.BASE_DIR, 'static', 'images/carousel_images')]
    for directory in image_dir:
        images.append(os.listdir(directory))

    context = {
        'events': events,
        'images': images
    }
    return render(request, 'base.html', context)

def events_list(request, category):
    events = Event.objects.filter(category=category)
    context = {'events': events}
    return render(request, 'base.html', context)

def event_detail(request, category, pk):
    events = get_object_or_404(Event, category=category, pk=pk)
    context = {
        'events': events
    }
    return render(request, 'booking/event_detail.html', context)

def ticket_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    tickets = set()

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            tickets = set(Event.objects.filter(title__icontains=search))
        else:
            cities = Place.objects.filter(location_city__icontains=search)
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
                return redirect('booking:index')

        messages.error(request, f'Invalid username or password')
        return render(request, 'booking/login.html', {'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('booking:index')




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