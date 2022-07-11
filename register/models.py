from django.db import models
from django.contrib.auth.models import User

from order.models import Cart, Order, OrdersDetail
from book.models import FavoriteBook


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    image = models.ImageField(upload_to='user_image')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    order_detail = models.ForeignKey(OrdersDetail, on_delete=models.CASCADE, null=True, blank=True)
    favorite = models.ForeignKey(FavoriteBook, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username