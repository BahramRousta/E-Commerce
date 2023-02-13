import pytest


class TestCartItems:

    @pytest.mark.django_db
    def test_create_cart_items(self, cart, cart_items):
        assert cart_items.cart == cart
        assert cart_items.book.title == "book"
        assert cart_items.quantity == 10
        assert cart_items.price == 10000

    @pytest.mark.django_db
    def test_should_str_method_return_book_title(self, cart_items):
        assert str(cart_items) == "book"

    @pytest.mark.django_db
    def test_cart_item_total_price(self, cart_items):
        assert cart_items.cart_item_price() == (10 * 10000)