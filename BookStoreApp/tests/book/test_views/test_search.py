import pytest
from django.urls import reverse


class TestSearch:
    base_url = reverse("book:search")

    def test_search_page(self, client):

        response = client.get(self.base_url)

        assert response.status_code == 200
        assert response.templates[0].name == "book/search.html"
        assert response.context["request"].path == "/search/"

    @pytest.mark.django_db
    def test_search_result_must_contain_book(self, client, book):
        response = client.get(self.base_url + f"?query={book.title}")

        assert response.status_code == 200
        assert len(response.context["results"]) == 1

    @pytest.mark.django_db
    def test_search_result_must_be_null(self, client):
        response = client.get(self.base_url + "?query=")

        assert response.status_code == 200
        assert len(response.context["results"]) == 0
