from django.shortcuts import render, redirect
from .models import Cart, CartItem
from accounts.models import Profile
from book.models import Book


def add_item_to_cart(request, slug):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    book = Book.objects.get(slug=slug)
    quantity = int(request.POST['quantity'])

    user_cart = Cart.objects.get(user=user_profile)
    if request.method == "POST":

        item = CartItem.objects.filter(book_id=book.id).first()
        print(item)


        if user_cart is not None:
            if item is not None:
                new_item_number = item.quantity + quantity

                item.quantity = new_item_number.save()

            else:
                new_item = CartItem.objects.create(cart=user_cart,
                                                   book=book,
                                                   price=book.price,
                                                   quantity=quantity)
        else:
            cart = Cart.objects.create(user=user_profile,
                                       is_paid=False)

            new_item = CartItem.objects.create(cart=cart,
                                               product=book,
                                               price=book.price,
                                               quantity=quantity)

        return redirect('book:book_detail', slug)
    else:
        return redirect('book:book_detail', slug)
