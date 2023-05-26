from django.urls import path
from .views import (
    CartItemCreateView,
    CartListView,
    DeleteCartItem,
    UpdateCartItem,
    ApplyCouponView,
    checkout_page,
    payment,
    do_pay
)

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('add_item_to_cart/<slug:slug>/', CartItemCreateView.as_view(), name='add_item_to_cart'),
    path('remove_cart_item/<int:pk>/', DeleteCartItem.as_view(), name='remove_cart_item'),
    path('update_cart/<int:pk>/', UpdateCartItem.as_view(), name='update_cart'),
    path('apply_coupon/', ApplyCouponView.as_view(), name='apply_coupon'),
    path('chechout_page/', checkout_page, name='checkout_page'),
    path('payment/', payment, name='payment'),
    path('do_pay/', do_pay, name='do_pay'),
]
