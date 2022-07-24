from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Cart, CartItem, Coupon
from accounts.models import Profile
from book.models import Book


@login_required()
def cart(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    user_cart = Cart.objects.get(username_id=user_profile.id, is_paid=False)
    cart_items = CartItem.objects.filter(cart=user_cart)

    return render(request, 'cart/cart.html', {'cart_items': cart_items,
                                                  'user_cart': user_cart})


@login_required()
def add_item_to_cart(request, slug):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    book = Book.objects.get(slug=slug)

    user_cart = Cart.objects.filter(username_id=user_profile.id).first()

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity < 1:
            quantity = 0

        item = CartItem.objects.filter(book_id=book.id, cart=user_cart).first()
        if user_cart is not None:
            if item is not None:
                CartItem.objects.filter(book_id=book.id, cart=user_cart).update(quantity=quantity)
            else:
                new_item = CartItem.objects.create(cart=user_cart,
                                                   book=book,
                                                   price=book.price,
                                                   quantity=quantity)
        else:
            cart = Cart.objects.create(user=user_profile,
                                       is_paid=False)

            new_item = CartItem.objects.create(cart=cart,
                                               book=book,
                                               price=book.price,
                                               quantity=quantity)

        return redirect('book:book_detail', slug)
    else:
        return redirect('book:book_detail', slug)


def update_cart(request, slug):
    book = Book.objects.get(slug=slug)
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_cart = Cart.objects.get(username_id=user_profile.id, is_paid=False)

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        print(quantity)

        # if quantity < 1:
        #     quantity = 0

        item = CartItem.objects.filter(book_id=book.id, cart=user_cart).update(quantity=quantity)
        print(item)
        return redirect('cart')
    else:
        return redirect('cart')


@login_required()
def remove_cart_item(request, slug):
    book = Book.objects.get(slug=slug)
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_cart = Cart.objects.get(username_id=user_profile.id, is_paid=False)
    cart_items = CartItem.objects.filter(cart=user_cart, book_id=book.id)
    item = cart_items
    item.delete()
    return redirect('cart')


def apply_coupon(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    user_cart = Cart.objects.get(username_id=user_profile.id, is_paid=False)
    now = timezone.now()

    coupon = None
    if request.method == "POST":
        coupon = request.POST['coupon']

        try:
            coupon = Coupon.objects.get(code__iexact=coupon,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            print(coupon)
            print(type(coupon.id))
            if coupon.id == user_cart.coupon.id:
                total_price = user_cart.get_total_price_after_discount()
                coupon.active = False
                coupon.save()

                return render(request, 'cart/cart.html', {'total_price': total_price,
                                                          'coupon': coupon})
        except Coupon.DoesNotExist:
            # raise ('کد تخفیف نامعتبر است.')
            return redirect('cart')
    else:
        return redirect('cart')
