from django.urls import path
from .views import add_item_to_cart

urlpatterns = [
    path('add_item_to_cart/<slug:slug>/', add_item_to_cart, name='add_item_to_cart')
]
