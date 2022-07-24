from django.urls import path
from .views import add_item_to_cart, cart, remove_cart_item, update_cart, apply_coupon

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add_item_to_cart/<slug:slug>/', add_item_to_cart, name='add_item_to_cart'),
    path('remove_cart_item/<slug:slug>/', remove_cart_item, name='remove_cart_item'),
    path('update_cart/<slug:slug>/', update_cart, name='update_cart'),
    path('apply_coupon/', apply_coupon, name='apply_coupon'),
]
