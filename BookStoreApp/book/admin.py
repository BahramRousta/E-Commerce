from django.contrib import admin
from .models import Book, Publisher, Author, Category, FavoriteBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['slug', 'published', 'publisher']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'website']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FavoriteBook)
class CategoryAdmin(admin.ModelAdmin):
    pass


