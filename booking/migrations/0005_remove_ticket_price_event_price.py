# Generated by Django 4.1.7 on 2023-05-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='price',
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.IntegerField(default=2023),
            preserve_default=False,
        ),
    ]
