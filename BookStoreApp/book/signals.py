from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from e_commerce.settings import base
from .models import *

CACHE_KEY_PREFIX = "custom_cache"


@receiver(post_delete, sender=Book)
@receiver(post_delete, sender=Author)
@receiver(post_delete, sender=Publisher)
@receiver(post_delete, sender=Category)
@receiver(post_delete, sender=FavoriteBook)
@receiver(post_delete, sender=SearchHistory)
def object_post_delete_handler(sender, **kwargs):
    """
    Delete all cache keys with the given prefix.
    """

    keys_pattern = f"views.decorators.cache.cache_*.{CACHE_KEY_PREFIX}.*.{base.LANGUAGE_CODE}.{base.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


@receiver(post_save, sender=Book)
@receiver(post_save, sender=Author)
@receiver(post_save, sender=Publisher)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=FavoriteBook)
@receiver(post_save, sender=SearchHistory)
def object_post_save_handler(sender, **kwargs):
    """
    Delete all cache keys with the given prefix.
    """

    keys_pattern = f"views.decorators.cache.cache_*.{CACHE_KEY_PREFIX}.*.{base.LANGUAGE_CODE}.{base.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)