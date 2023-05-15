from django.contrib import auth
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
import random
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime
from datetime import date


class Place(models.Model):
    CATEGORY_CHOICES = [
        ('cinema', 'Cinema'),
        ('theatre', 'Theatre'),
        ('concert', 'Concert')
    ]
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    city = models.CharField(max_length=120, default='Almaty')

    def __str__(self):
        return self.name


def validate_date(value):
    today = datetime.date.today()
    if value < today:
        raise ValidationError(
            _('Date cannot be in the past')
        )


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('performance', 'Performance'),
        ('show', 'Show')
    ]


    venue = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    start_time = models.TimeField()
    year_of_release = models.IntegerField()
    country = models.CharField(max_length=120)
    directors = models.CharField(max_length=100)
    stars = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    age_limit = models.IntegerField()
    date = models.DateField(validators=[validate_date], default=date(2023, 5, 18))
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

    def save(self, *args, **kwargs):
        if self.venue.category == 'cinema':
            self.category = 'movie'
        elif self.venue.category == 'performance':
            self.category = 'performance'
        elif self.venue.category == 'show':
            self.category = 'show'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    row = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.event.title


class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    photo_profile = models.ImageField(null=True, blank=True, upload_to="profile_photos/")
    balance = models.IntegerField()
    card_number = models.CharField(max_length=16)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True, choices=GENDER_CHOICES)
    country = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate random balance for new instances
            self.balance = random.randint(10000, 100000)
        super().save(*args, **kwargs)

    def empty_fields(self):
        fields = [
            self.avatar,
            self.phone_number,
            self.gender,
            self.country,
            self.user.first_name,
            self.user.last_name,
            self.user.email
        ]
        print(fields)
        empty_count = sum(
            field is None or (isinstance(field, str) and len(field.strip()) == 0)
            for field in fields
        )
        return empty_count

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profile'


class Purchase(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    card_num = models.CharField(max_length=16)
    email = models.EmailField()
    number = models.CharField(max_length=12)


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True,
                                       help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              help_text="The Book that this review is for.")

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.event.title)
