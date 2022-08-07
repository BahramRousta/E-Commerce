from rest_framework import serializers
from comment.serializers import CommentSerializer
from book.models import Book, Category, Author, Publisher


class AuthorUnrelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookUnrelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        exclude = ['id']


class PublisherUnrelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class CategoryUnrelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    book_comment = CommentSerializer(many=True, read_only=True)
    authors = AuthorUnrelatedSerializer(write_only=True, required=False, many=True)
    publishers = PublisherUnrelatedSerializer(write_only=True, required=False)
    categories = CategoryUnrelatedSerializer(write_only=True, required=False)

    class Meta:
        model = Book
        exclude = ['id']
        extra_kwargs = {'author': {'required': False},
                        'publisher': {'required': False},
                        'category': {'required': False}}

    def create(self, validated_data):
        try:
            categories = validated_data.pop('categories')
            authors = validated_data.pop('authors')
            publishers = validated_data.pop('publishers')

            new_book = Book.objects.create(**validated_data)

            for author in authors:
                new_author = Author.objects.create(**author)
                new_book.author.add(new_author)

            new_category = Category.objects.create(**categories)
            new_book.category = new_category

            new_publisher = Publisher.objects.create(**publishers)
            new_book.publisher = new_publisher
            new_book.save()

            return new_book
        except:
            author = validated_data.pop('author')
            new_book = Book.objects.create(**validated_data)
            new_book.author.add(author[0])
            new_book.save()
            return new_book


class CategorySerializer(serializers.ModelSerializer):
    book_categories = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """
        Get authors list with themselves books.
        Also use to add author and book in the sametime.
    """

    # Get authors book
    authors_book = BookSerializer(many=True, read_only=True)
    # Post book sametime you enter author in DB
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


class PublisherSerializer(serializers.ModelSerializer):
    book_publisher = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = '__all__'

