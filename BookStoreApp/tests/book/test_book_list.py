import pytest
from django.urls import reverse


class TestBookList:

    @pytest.mark.django_db
    def test_home_page(self, db, book, client):
        home_page_url = reverse('book:book_list')
        response = client.get(home_page_url)

        assert response.status_code == 200
        assert response.templates[0].name == "book/index.html"
        assert response.context["request"].path == "/"

    def test_must_dont_have_new_publish_book(self, db, client):
        home_page_url = reverse('book:book_list')
        response = client.get(home_page_url)

        assert len(response.context['new_publish_book']) == 0