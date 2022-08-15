from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from cart.models import Cart
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=Profile)
# def create_cart(sender, instance, created, **kwargs):
#     if created:
#         Cart.objects.create(username=instance)
#
#
# @receiver(post_save, sender=Profile)
# def save_cart(sender, instance, **kwargs):
#     instance.user_cart.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

