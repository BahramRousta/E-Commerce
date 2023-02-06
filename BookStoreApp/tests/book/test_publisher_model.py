import pytest
from django.db import IntegrityError
from book.models import Publisher


class TestPublisherModel:

    @pytest.mark.django_db
    def test_should_create_successfully_new_publisher(self, publisher):
        assert Publisher.objects.count() == 1
        assert publisher.name == "publisher"
        assert publisher.slug == "publisher"

    @pytest.mark.django_db
    def test_should_fail_create_duplicate_publisher(self, publisher):
        with pytest.raises(IntegrityError) as model_ex:
            Publisher.objects.create(name=publisher.name,
                                     slug=publisher.slug)
        assert 'duplicate key value violates unique constraint "book_publisher_slug_key"' in str(model_ex)
