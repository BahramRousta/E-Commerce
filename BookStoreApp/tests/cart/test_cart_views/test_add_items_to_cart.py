from django.urls import reverse


class TestAddItemToCart:

    def setup_method(self):
        pass

    def test_add_new_item_to_cart(self, db, client, user, book):
        client.force_login(user)
        self.url = reverse("add_item_to_cart", args=[book.slug])
        payload = {
            "quantity": 1
        }
        response = client.post(self.url, payload)

        assert response.status_code == 302
