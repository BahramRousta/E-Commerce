import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestBookList:

    def setup_method(self):
        self.home_page_url = reverse('book:home_page')

    def test_home_page(self, client):
        response = client.get(self.home_page_url)

        assert response.status_code == 200
        assert response.templates[0].name == "book/index.html"
        assert response.context["request"].path == "/"

    def test_must_dont_have_a_newly_published_book(self, client):

        response = client.get(self.home_page_url)

        assert len(response.context['new_publish_book']) == 0
        assert len(list(response.context['authors'])) == 0
        assert response.context['tag'] is None

    def test_must_have_a_newly_published_book(self, book, client):

        response = client.get(self.home_page_url)

        assert len(response.context['new_publish_book']) != 0
