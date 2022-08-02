from django.db import models
from django.contrib.auth.models import User
from book.models import FavoriteBook


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='user_image', null=True, blank=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=13, null=True)

    def __str__(self):
        return f'{self.user}'