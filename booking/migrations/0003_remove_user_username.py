# Generated by Django 4.1.7 on 2023-05-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_movie_age_limit_alter_movie_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
