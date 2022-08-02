from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager


class Publisher(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=100,
                            unique=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    website = models.URLField(null=True,
                              blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    email = models.EmailField(db_index=True, null=True, blank=True)
    image = models.ImageField(upload_to='author_images',
                              blank=True,
                              null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Category(models.Model):
    name = models.CharField(max_length=50,
                            db_index=True)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class BookManager(models.Manager):
    def get_best_seller(self):
        return self.get_queryset().all().order_by('count_sold')[:8]


class Book(models.Model):
    title = models.CharField(max_length=500,
                             db_index=True)
    slug = models.SlugField(max_length=500,
                            unique=True)
    author = models.ManyToManyField(Author, related_name='authors_book')
    isbn = models.CharField(max_length=13, null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_images',
                                    blank=True,
                                    null=True)
    published = models.DateField(auto_now=False,
                                 auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book_categories')
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    language = models.CharField(max_length=25,
                                blank=True,
                                null=True)
    new_publish = models.BooleanField(default=False, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=True)
    count_sold = models.IntegerField(default=0, null=True, blank=True)
    tags = TaggableManager()
    objects = BookManager()

    class Meta:
        ordering = ['-published']
        index_together: (('id', 'slug'),)

    # def new_publish(self):
    #     self.new_publish = False
    #     if self.published - timezone.now() <30:
    #         self.new_publish = True

    def __str__(self):
        return self.title


class FavoriteBook(models.Model):
    user = models.CharField(max_length=25)
    book = models.ForeignKey(Book, on_delete=models. CASCADE,
                             related_name='favorite',
                             null=True, blank=True)

    def __str__(self):
        return self.book.title


class SearchHistory(models.Model):
    user_id = models.IntegerField(null=True)
    query = models.CharField(max_length=100)

