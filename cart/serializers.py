from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cart.models import CartItem, Cart, Coupon


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['book', 'quantity']

    def validate_quantity(self, value):
        if value >= 1:
            return value

        raise ValidationError('Quantity must be at least one.')


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['code']


class CouponPostSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, write_only=True)
