from django.db import models
from django.contrib.auth.models import AbstractUser


class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    cinema_name = models.CharField(max_length=100)
    location_city = models.CharField(max_length=100)

    def __str__(self):
        return self.cinema_name


class Movie(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    year_of_release = models.IntegerField()
    country = models.CharField(max_length=120)
    directors = models.CharField(max_length=100)
    stars = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    age_limit = models.IntegerField()
    release_date = models.DateField()
    description = models.TextField()
    hall_id = models.IntegerField()
    rating = models.IntegerField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


class Ticket(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    time = models.DateTimeField()
    seat = models.DecimalField(max_digits=8, decimal_places=2)
    row = models.IntegerField()

    def __str__(self):
        return self.movie_name


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    birthday_date = models.DateTimeField()
    photo_profile = models.ImageField(null=True, blank=True, upload_to="profile_photos/")
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    card_number = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    card_num = models.CharField(max_length=16)
    email = models.EmailField()
    number = models.CharField(max_length=12)
