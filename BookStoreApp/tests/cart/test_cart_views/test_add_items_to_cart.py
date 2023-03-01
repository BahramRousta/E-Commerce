from django.urls import reverse

from cart.models import CartItem, Cart


class TestAddItemToCart:

    def setup_method(self):
        pass

    def test_add_new_item_to_cart(self, db, client, user, book):
        client.force_login(user)
        self.url = reverse("add_item_to_cart", args=[book.slug])
        payload = {
            "quantity": 10
        }
        response = client.post(self.url, payload)

        assert response.status_code == 302
        assert CartItem.objects.filter(cart=user.user_cart).count() == 1
        assert CartItem.objects.get(book=book, cart=user.user_cart).quantity == 10