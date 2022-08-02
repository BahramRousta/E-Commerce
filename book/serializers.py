from rest_framework import serializers
from book.models import Book, Category, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    book_categories = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    authors_book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'

