from django.http import Http404
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
    try:
        user_cart = Cart.objects.filter(user_id=user_profile.id, is_paid=False).first()
    except:
        user_cart = Cart.objects.create(user_id=user_profile.id, is_paid=False)
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'cart/cart.html', {'cart_items': cart_items,
                                              'user_cart': user_cart})


@login_required()
def add_item_to_cart(request, slug):
    user = request.user

    book = Book.objects.get(slug=slug)

    user_cart = Cart.objects.filter(user=user, is_paid=False).first()

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
            cart = Cart.objects.create(username=user_profile,
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
    user_cart = Cart.objects.get(user=user, is_paid=False)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity < 1:
            quantity = 0

        item = CartItem.objects.filter(book_id=book.id, cart=user_cart).update(quantity=quantity)
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

    user_cart = Cart.objects.get(user=user, is_paid=False)
    cart_items = CartItem.objects.filter(cart=user_cart)

    now = timezone.now()

    coupon = None
    if request.method == "POST":
        coupon = request.POST['coupon']

        try:
            user_coupon = Coupon.objects.get(code__iexact=coupon,
                                             valid_from__lte=now,
                                             valid_to__gte=now,
                                             active=True)
            if user_cart.id == user_coupon.carts.select_related().first().id:
                total_price = user_cart.get_total_price_after_discount()

                if user_cart.is_paid == True:
                    coupon.active = False
                    coupon.save()

                return render(request, 'cart/cart.html', {'total_price': total_price,
                                                          'coupon': coupon,
                                                          'cart_items': cart_items,
                                                          'user_cart': user_cart})
            else:
                raise Http404('کد تخفیف نامعتبر است.')
        except Coupon.DoesNotExist:
            raise Http404('کد تخفیف نامعتبر است.')
    else:
        return redirect('cart')


def checkout_page(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_cart = Cart.objects.get(username_id=user_profile.id, is_paid=False)
    cart_items = CartItem.objects.filter(cart=user_cart)
    return render(request, 'cart/checkout.html', {'user_profile': user_profile,
                                                  'user_cart': user_cart,
                                                  'cart_items': cart_items})


def payment(request):
    return render(request, 'cart/payment.html')


def do_pay(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_cart = Cart.objects.filter(username_id=user_profile.id, is_paid=False)
    user_cart.update(is_paid=True)
    # user_cart.save()
    return redirect('shop:books_list')
