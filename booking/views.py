from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Place, Event, Ticket, User, Purchase, Review
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, SearchForm, ReviewForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .utils import average_rating
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
            return redirect('booking:index')
        else:
            return render(request, 'booking/register.html', {'form': form})

def event_detail(request, category, pk):
    events = get_object_or_404(Event, category=category, pk=pk)
    reviews = events.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "events": events,
            "event_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "events": events,
            "book_rating": None,
            "reviews": None
        }
    return render(request, 'booking/event_detail.html', context)

@login_required
def review_edit(request, event_pk, review_pk=None):
    events = get_object_or_404(Event, pk=event_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, event_id=event_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.event = events

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(events))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(events))

            updated_review.save()
            return redirect("booking:event_detail",events.category, events.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "booking/instance-form.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": events,
                   "related_model_type": events.category
                   })