# Generated by Django 4.0.6 on 2022-08-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('logo', models.ImageField(upload_to='shop_logo')),
                ('description', models.TextField()),
            ],
        ),
    ]
