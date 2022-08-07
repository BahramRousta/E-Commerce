from django.db import models
from django.contrib.auth.models import User
from book.models import FavoriteBook

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='user_image', null=True, blank=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=13, null=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

