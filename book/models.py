from typing import Tuple

from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=100,
                            unique=True)
    address = models.CharField(max_length=250)
    website = models.URLField(null=True,
                              blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    email = models.EmailField(db_index=True)
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


class Book(models.Model):
    title = models.CharField(max_length=500,
                             db_index=True)
    slug = models.SlugField(max_length=500,
                            unique=True)
    author = models.ManyToManyField(Author)
    isbn = models.CharField(max_length=13)
    cover_image = models.ImageField(upload_to='book_images',
                                    blank=True,
                                    null=True)
    published = models.DateField(auto_now=False,
                                 auto_now_add=False)
    genre = models.ManyToManyField(Category,
                                   related_name='books')
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    language = models.CharField(max_length=25,
                                blank=True,
                                null=True)

    class Meta:
        ordering = ['-published']
        index_together: (('id', 'slug'),)

    def __str__(self):
        return self.title
