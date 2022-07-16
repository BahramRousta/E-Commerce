from django.shortcuts import render
from django.views.generic import ListView

from book.models import Book, Category, Publisher


class BooksList(ListView):
    template_name = 'shop/books_list.html'
    paginate_by = 6
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['publishers'] = Publisher.objects.all()


        return context

# def books_list(request):
#     books = Book.objects.filter(available=True)
#     return render(request, 'shop/books_list.html', {'books': books})

