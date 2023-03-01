import pytest
from django.db import IntegrityError

from book.models import Author


class TestAuthorModel:

    @pytest.mark.django_db
    def test_should_create_successfully_new_author(self, author):
        assert Author.objects.count() == 1
        assert author.name == "author"
        assert author.slug == "author"

    @pytest.mark.django_db
    def test_should_fail_create_duplicate_author(self, author):
        with pytest.raises(IntegrityError) as model_ex:
            Author.objects.create(name=author.name,
                                  slug=author.slug)
        assert 'duplicate key value violates unique constraint "book_author_slug_key"' in str(model_ex)
