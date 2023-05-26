from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Cart, CartItem, Coupon
from accounts.models import Profile
from book.models import Book


class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, is_paid=False).first()
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


class DeleteCartItem(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart')

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        item_id = self.kwargs['pk']
        return queryset.filter(id=item_id, cart__user=user, cart__is_paid=False)


class ApplyCouponView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            received_coupon = request.POST.get('coupon')
        except KeyError:
            return redirect('cart')

        now = timezone.now()

        coupon = Coupon.objects.filter(cart__user=self.request.user,
                                       code__iexact=received_coupon,
                                       valid_from__lte=now,
                                       valid_to__gte=now,
                                       active=True).first()
        if coupon is not None:
            coupon.cart.get_total_price_after_discount()
            if coupon.cart.is_paid:
                coupon.active = False
                coupon.save()
            return redirect('cart')
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
