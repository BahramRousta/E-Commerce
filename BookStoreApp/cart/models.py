from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from book.models import Book
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_cart')
    is_paid = models.BooleanField(default=False)

    def cart_total_price(self):
        total = 0
        for cart_item in self.cartitems.all():
            total += (cart_item.price * cart_item.quantity)
        return int(total)

    def get_discount(self):
        for coupon in self.coupon.all():
            return (coupon.discount / 100) * self.cart_total_price()

    def get_total_price_after_discount(self):
        return self.cart_total_price() - self.get_discount()

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='cartitems')
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name='books')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def cart_item_price(self):
        return int(self.price * self.quantity)

    def __str__(self):
        return self.book.title


class Coupon(models.Model):
    code = models.CharField(max_length=20,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)])
    active = models.BooleanField()
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='coupon',
                             null=True,
                             blank=True)

    def __str__(self):
        return self.code