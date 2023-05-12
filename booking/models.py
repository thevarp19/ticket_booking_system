from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year_of_release = models.IntegerField(default=1)
    # distributor = models.CharField(max_length=100)
    country_of_production = models.CharField(max_length=100)
    director = models.CharField(max_length=100, default='')
    cast = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    age_limit = models.IntegerField()
    premiere_date = models.DateField()
    description = models.TextField()
class Theater(models.Model):
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    artists = models.CharField(max_length=200)
    date = models.DateField()
    start = models.TimeField()
    age_limit = models.IntegerField()
    description = models.TextField()

class Concert(models.Model):
    artist = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    start = models.TimeField()
    artists = models.CharField(max_length=200)
    age_limit = models.IntegerField()
    description = models.TextField()

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    row = models.CharField(max_length=5)
    number = models.IntegerField()

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
