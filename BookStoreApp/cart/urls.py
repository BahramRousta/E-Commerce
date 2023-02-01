from django.urls import path
from .views import (
    add_item_to_cart,
    cart,
    remove_cart_item,
    update_cart,
    apply_coupon,
    checkout_page,
    payment,
    do_pay
)

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add_item_to_cart/<slug:slug>/', add_item_to_cart, name='add_item_to_cart'),
    path('remove_cart_item/<slug:slug>/', remove_cart_item, name='remove_cart_item'),
    path('update_cart/<slug:slug>/', update_cart, name='update_cart'),
    path('apply_coupon/', apply_coupon, name='apply_coupon'),
    path('chechout_page/', checkout_page, name='checkout_page'),
    path('payment/', payment, name='payment'),
    path('do_pay/', do_pay, name='do_pay'),
]
