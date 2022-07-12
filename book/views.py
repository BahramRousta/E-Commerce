from django.shortcuts import render
from .models import Book


def index(request):
    books = Book.objects.filter(new_publish=True)
    return render(request, 'book/index.html', {'books': books})

