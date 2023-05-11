from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from booking.models import Movie
from .utils import average_rating
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
from django.contrib import messages


from booking.forms import MovieForm



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




def movie_list(request):
    movies = Movie.objects.all()
    movies_with_reviews = []
    for movie in movies:
        reviews = movie.review_set.all()
        if reviews:
            movie_rating = average_rating([movie.rating for movie in reviews])
            number_of_reviews = len(reviews)
        else:
            movie_rating = None
            number_of_reviews = 0
        movies_with_reviews.append({"movie": movie, "movie_rating": movie_rating, "number_of_reviews": number_of_reviews})

    context = {
        "movie_list": movies_with_reviews
    }
    return render(request, "movie_list.html", context)


def movie_media(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.FILES, instance=movie)
        img = form.cleaned_data.get("image")
        if img:
            image = Image.open(img)
            image.thumbnail((300, 300))
            image_data = BytesIO()
            image.save(fp=image_data, format=img.image.format)
            image_file = ImageFile(image_data)
            movie.image.save(img.name, image_file)
        movie.save()
        messages.success(request, "Movie \"{}\" was successfully updated.".format(movie))
        return redirect("movie_detail", movie.pk)
    else:
        form = MovieForm(instance=movie)

    return render(request, "instance-form.html")

# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     reviews = movie.review_set.all()
#     if reviews:
#         context = {
#             "book": book
#             "reviews": reviews
#         }
#     else:
#         context = {
#             "book": book,
#             "book_rating": None,
#             "reviews": None
#         }
    # if request.user.is_authenticated:
    #     max_viewed_books_length = 10
    #     viewed_books = request.session.get('viewed_books', [])
    #     viewed_book = [book.id, book.title]
    #     if viewed_book in viewed_books:
    #         viewed_books.pop(viewed_books.index(viewed_book))
    #     viewed_books.insert(0, viewed_book)
    #     viewed_books = viewed_books[:max_viewed_books_length]
    #     request.session['viewed_books'] = viewed_books
    # return render(request, "reviews/book_detail.html", context)




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