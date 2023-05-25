from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from .models import Cart, CartItem, Coupon
from accounts.models import Profile
from book.models import Book


class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(cart__user=self.request.user, cart__is_paid=False).select_related('book')
        return queryset


class CartItemCreateView(LoginRequiredMixin, View):
    model = CartItem
    success_url = 'book:book_detail'

    def get_user_cart(self):
        user = self.request.user
        return Cart.objects.filter(user=user, is_paid=False).first()

    def post(self, request, slug, *args, **kwargs):
        quantity = self.request.POST.get('quantity')
        if int(quantity) < 1:
            quantity = 0

        book = get_object_or_404(Book, slug=self.kwargs.get('slug'))

        CartItem.objects.update_or_create(
            book=book,
            cart=self.get_user_cart(),
            defaults={'quantity': quantity}
        )

        return redirect(self.success_url, slug)


class UpdateCartItem(UpdateView):
    model = CartItem
    fields = ['quantity']
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        if form.instance.quantity < 1:
            form.instance.quantity = 0

        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        item_id = self.kwargs['pk']
        return queryset.filter(id=item_id, cart__user=user, cart__is_paid=False)



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
