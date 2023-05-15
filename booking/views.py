from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from . import models
from .models import Place, Event, Ticket, Profile, Purchase, Review
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, SearchForm, ReviewForm, ConfirmPurchase, ValidatePurchase
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .utils import average_rating
import os
from django.conf import settings
import random

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
    images = []
    image_dir = [os.path.join(settings.BASE_DIR, 'static', 'images/carousel_images')]
    for directory in image_dir:
        images.append(os.listdir(directory))
    context = {'events': events,
               'images': images
               }
    return render(request, 'base.html', context)


def event_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    events = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            events = Event.objects.filter(title__iregex=search)

        if request.user.is_authenticated:
            search_history.append([search_in, search])
            request.session['search_history'] = search_history
    elif search_history:
        initial = dict(search=search_text,
                       search_in=search_history[-1][0])
        form = SearchForm(initial=initial)

    return render(request, "booking/search-results.html", {"form": form, "search_text": search_text, "events": events})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'booking/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            print(request.user)
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('index')

        messages.error(request, f'Invalid username or password')
        return render(request, 'booking/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'booking/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'booking/register.html', {'form': form})


def event_detail(request, category, pk):
    events = get_object_or_404(Event, category=category, pk=pk)
    reviews = events.review_set.all()
    if reviews:
        event_rating = average_rating([review.rating for review in reviews])
        context = {
            "events": events,
            "event_rating": event_rating,
            "reviews": reviews
        }
    else:
        context = {
            "events": events,
            "event_rating": None,
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
            updated_review.creator = request.user

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(events))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(events))

            updated_review.save()
            return redirect("event_detail", events.category, events.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "booking/instance-form.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": events,
                   "related_model_type": events.category
                   })


def profile_page(request):
    if request.user:
        profile = models.Profile.objects.filter(user=request.user).first()
        if not profile:
            Profile.objects.create(user=request.user)

        context = {
            'profile': profile,
            'empty_fields': profile.empty_fields(),
            'completion_percentage': int(100 - (profile.empty_fields() / 7 * 100))
        }

        return render(request, 'booking/profile.html', context)
    else:
        return HttpResponse('', status=404)


def edit_profile(request):
    # Retrieve the client profile
    try:
        client = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Handle the case when the client profile doesn't exist
        messages.error(request, 'Client profile does not exist.')
        return redirect('edit-profile')

    activity_gender_type = Profile.GENDER_CHOICES
    activity_gender_type_result = []
    for gender_type in activity_gender_type:
        for gender in gender_type:
            activity_gender_type_result.append(gender)
    activity_gender_type_result = list(set(activity_gender_type_result))

    # POST DATA: Profile contacts
    if request.method == 'POST' and 'first_name' in request.POST:
        avatar = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        card_pin = request.POST.get('card')
        gender = request.POST.get('gender')

        if not (first_name and last_name):
            messages.error(request, 'First name and last name are required.')
        else:
            # Update the client profile
            client.avatar = avatar
            client.phone_number = phone_number
            client.gender = gender
            client.country = country
            client.card_number = card_pin

            client.save()

            # Update the associated User model
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return redirect('edit-profile')
    # POST DATA: Change Email contacts
    if request.method == 'POST' and 'new_email' in request.POST:
        new_email = request.POST.get('new_email')
        confirm_password = request.POST.get('confirm_password')

        if client.user.check_password(confirm_password):
            # Check if email is already in use by another user
            if User.objects.filter(Q(email=new_email) & ~Q(id=request.user.id)).exists():
                messages.error(request, 'Email address already in use.')
            else:
                User.objects.filter(id=request.user.id).update(email=new_email)
        else:
            messages.error(request, 'Invalid password')

        return redirect('edit-profile')

    # POST DATA: Change Password contacts
    if request.method == 'POST' and 'new_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if client.user.check_password(current_password):
            user = Profile.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # update session
        else:
            messages.error(request, 'Invalid password.')

        return redirect('edit-profile')

    context = {
        'profile': client,
        'activity_gender_type': activity_gender_type_result,
        'empty_fields': client.empty_fields() if client else 0,
        'completion_percentage': int(100 - (client.empty_fields() / 7 * 100)) if client else 0
    }

    return render(request, 'booking/edit-profile.html', context)


def purchase_movie(request, pk):
    rows = [
        [{"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False},
         {"occupied": False}, {"occupied": False}, {"occupied": False}],
        [{"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False},
         {"occupied": False}, {"occupied": False}, {"occupied": False}],
        [{"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False}, {"occupied": False},
         {"occupied": False}, {"occupied": False}, {"occupied": False}],
    ]
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        for seat_group in selected_seats:
            seat_pairs = seat_group.split(',')
            for seat_pair in seat_pairs:
                row, seat = seat_pair.split('-')
                row = int(row)
                seat = int(seat)
                print(row, seat)
                event = Event.objects.get(pk=pk)
                rows[row][seat] = {"occupied": True}
                ticket = Ticket(event=event, seat=seat, row=row)  # Set the price accordingly
                ticket.save()

    # Loop over the selected seats and rows and create Ticket objects
    # for seat, row in zip(selected_seats, selected_rows):
    #     ticket = Ticket(price=0, seat=seat, row=row)  # Replace 0 with the actual ticket price
    #     ticket.save()

    # ticket_price = int(request.POST.get('ticket_price'))
    # movie_index = int(request.POST.get('movie_index'))
    # set_movie_data(request.session, movie_index, ticket_price)
    # return JsonResponse({'success': True})

    movie = get_object_or_404(Event, pk=pk)

    # selected_seats = request.session.get('selected_seats', [])
    # selected_movie_index = request.session.get('selected_movie_index')

    # if selected_seats:
    #     for row in rows:
    #         for seat in row:
    #             seat['selected'] = True if rows.index(row) in selected_seats and not seat['occupied'] else False

    context = {
        'movie': movie,
        'rows': rows
        #     'selected_seats_count': len(selected_seats),
        #     'total_price': len(selected_seats) * int(request.session.get('ticket_price', 0)),
        #     'selected_movie_index': selected_movie_index,
        #     'ticket_price': int(request.session.get('ticket_price', 0))
    }
    return render(request, 'booking/events_seats.html', context)


def validate_purchase(request):
    if request.method == "GET":
        form = ValidatePurchase()
    else:
        form = ValidatePurchase(request.POST)
        if form.is_valid():
            random_number = random.randint(1000, 9999)
            email_from = form.cleaned_data['email']
            card_num = form.cleaned_data['card_num']
            send_mail("Write this code: ", str(random_number), email_from, ['rustembekov2003@gmail.com', email_from])
            return HttpResponseRedirect(
                reverse('purchase_confirm') + f'?password={random_number}&card_num={card_num}')
    return render(request, 'booking/validate_purchase.html', {'form': form})


def purchase_confirm(request):
    user = Profile.objects.get(user=request.user)
    print(user.card_number)  # Ensure that this prints the correct card number
    form = ConfirmPurchase(request.GET)
    if form.is_valid():
        password = form.cleaned_data["password"]
        card_num = form.cleaned_data["card_num"]
        inp_pass = form.cleaned_data["inp_pass"]
        if inp_pass == password and card_num == user.card_number:
            return HttpResponseRedirect(reverse('purchase_movie') + f'?is_valid={True}')
        else:
            messages.success(request, "Please try again")
            redirect('purchase_confirm')
    return render(request, "booking/purchase_confirm.html", {'form': form})
