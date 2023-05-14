from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models



class Place(models.Model):
    CATEGORY_CHOICES = [
        ('cinema', 'Cinema'),
        ('theatre', 'Theatre'),
        ('concert', 'Concert')
    ]
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


    def __str__(self):
        return self.name


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('performance', 'Performance'),
        ('show', 'Show')
    ]

    venue = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
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
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if self.venue.category == 'cinema':
            self.category = 'movie'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    seat = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    row = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.event.name


class User(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
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