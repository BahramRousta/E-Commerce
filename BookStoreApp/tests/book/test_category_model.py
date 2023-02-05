import pytest
from django.db import IntegrityError
from book.models import Category


class TestCategoryModel:

    @pytest.mark.django_db
    def test_should_create_new_category_successfully(self, category):
        assert Category.objects.count() == 1
        assert category.name == "category"
        assert category.slug == "category"

    @pytest.mark.django_db
    def test_should_fail_create_duplicate_category(self, category):
        with pytest.raises(IntegrityError) as model_ex:
            Category.objects.create(name=category.name,
                                    slug=category.slug)

        assert 'duplicate key value violates unique constraint "book_category_slug_key"' in str(model_ex)