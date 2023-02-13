import pytest
from cart.models import Cart


@pytest.mark.django_db
class TestCartModel:

    def test_create_user_cart(self, user):
        assert Cart.objects.count() == 1
        assert not user.user_cart.is_paid

    def test_should_cart_str_method_return_user_username(self, user):
        cart = Cart.objects.get(user_id=user.id)
        assert str(cart) == user.username

    def test_cart_total_price(self, cart, cart_items):
        assert cart.cart_total_price() == 100000

    def test_cart_get_discount(self, cart, cart_items, coupon):
        assert cart.get_discount() == 10000.0

    def test_cart_get_total_price_after_discount(self, cart, cart_items, coupon):
        assert cart.get_total_price_after_discount() == 90000.0
