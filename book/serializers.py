from rest_framework import serializers
from book.models import Book, Category, Author


class AuthorUnrelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    book_author = AuthorUnrelatedSerializer(many=True, read_only=True)
    new_author = AuthorUnrelatedSerializer(write_only=True)
    new_author2 = AuthorUnrelatedSerializer(write_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {'author': {'required': False}}

    def create(self, validated_data):
        try:
            new_author2 = validated_data.pop('new_author2')
            new_author = validated_data.pop('new_author')
            new_book = Book.objects.create(**validated_data)
            author = Author.objects.create(**new_author)
            author2 = Author.objects.create(**new_author2)
            new_book.author.add(author, author2)
            return new_book
        except:
            new_author = validated_data.pop('new_author')
            new_book = Book.objects.create(**validated_data)
            author = Author.objects.create(**new_author)
            new_book.author.add(author)
            return new_book


# class CategorySerializer(serializers.ModelSerializer):
#     book_categories = BookSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Category
#         fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    # Get authors book
    authors_book = BookSerializer(many=True, read_only=True)
    # Can to create book same time you enter author in DB
    book = BookSerializer(write_only=True)

    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        book = validated_data.pop('book')
        author = Author.objects.create(**validated_data)
        new_book = Book.objects.create(**book)
        new_book.author.add(author)
        return author

