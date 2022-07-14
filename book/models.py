from django.db import models
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


class Book(models.Model):
    title = models.CharField(max_length=500,
                             db_index=True)
    slug = models.SlugField(max_length=500,
                            unique=True)
    author = models.ManyToManyField(Author)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_images',
                                    blank=True,
                                    null=True)
    published = models.DateField(auto_now=False,
                                 auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    language = models.CharField(max_length=25,
                                blank=True,
                                null=True)
    new_publish = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    count_sold = models.IntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ['-published']
        index_together: (('id', 'slug'),)

    # def new_publish(self):
    #     self.new_publish = False
    #     if self.published - timezone.now() <30:
    #         self.new_publish = True
    #
    # def best_seller(self):
    #     self.best_seller_book = Book.objects.all().order_by('count_sold')[:8]
    #     return self.best_seller_book

    def __str__(self):
        return self.title


class FavoriteBook(models.Model):
    book_id = models.IntegerField()