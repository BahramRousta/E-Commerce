# Generated by Django 4.0.6 on 2022-07-14 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_remove_book_new_publish_book_count_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='new_publish',
            field=models.BooleanField(default=False),
        ),
    ]
