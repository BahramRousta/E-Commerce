from django.db import models
from book.models import Book
from accounts.models import Profile


class Cart(models.Model):
    username = models.OneToOneField(Profile, on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        total = 0
        for cart_item in self.cartitems.all():
            total += (cart_item.price * cart_item.quantity)
        return int(total)

    # def __str__(self):
    #     return self.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT,
                             related_name='cartitems')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return int(self.price * self.quantity)

    def __str__(self):
        return self.book.title

