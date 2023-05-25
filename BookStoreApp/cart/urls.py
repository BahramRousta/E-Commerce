from django.urls import path
from .views import (
    CartItemCreateView,
    CartListView,
    remove_cart_item,
    update_cart,
    apply_coupon,
    checkout_page,
    payment,
    do_pay
)

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('add_item_to_cart/<slug:slug>/', CartItemCreateView.as_view(), name='add_item_to_cart'),
    path('remove_cart_item/<slug:slug>/', remove_cart_item, name='remove_cart_item'),
    path('update_cart/<slug:slug>/', update_cart, name='update_cart'),
    path('apply_coupon/', apply_coupon, name='apply_coupon'),
    path('chechout_page/', checkout_page, name='checkout_page'),
    path('payment/', payment, name='payment'),
    path('do_pay/', do_pay, name='do_pay'),
]
