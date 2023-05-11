from django.db import models


class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    cinema_name = models.CharField(max_length=100)
    location_city = models.CharField(max_length=100)

    def __str__(self):
        return f"Cinema {self.id}"


class Movie(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    release_date = models.DateField()
    genre = models.CharField(max_length=120)
    stars = models.CharField(max_length=100)
    duration = models.FloatField()
    hall_id = models.DecimalField(max_digits=8, decimal_places=2)
    start_time = models.TimeField()
    rating = models.IntegerField()

    def __str__(self):
        return self.title


class Ticket(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    time = models.DateTimeField()
    seat = models.DecimalField(max_digits=8, decimal_places=2)
    row = models.IntegerField()

    def __str__(self):
        return f"Ticket {self.id}"


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    birthday_date = models.DateTimeField()
    photo_profile = models.ImageField(upload_to='images/')
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    card_number = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    card_num = models.CharField(max_length=16)
    email = models.EmailField()
    number = models.CharField(max_length=12)
