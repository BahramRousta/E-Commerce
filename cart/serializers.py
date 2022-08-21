from rest_framework import serializers
from cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['book', 'quantity']

