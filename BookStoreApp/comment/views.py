from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from .models import Comment, Reply
from book.models import Book


class CommentCreateView(CreateView):
    model = Comment
    fields = ['username', 'email', 'body']

    def form_valid(self, form):
        book = Book.objects.get(slug=self.kwargs['slug'])
        form.instance.book = book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book:book_detail', kwargs={'slug': self.kwargs['slug']})


class CommentListView(ListView):
    model = Comment
    template_name = 'book/book_detail.html'
    context_object_name = 'comments'

    def get_queryset(self):
        comments = Comment.objects.select_related('book').get(book__slug=self.kwargs['slug'])
        return comments


def reply_comment(request, comment_id, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.method == "POST":
        reply = request.POST['body']
        comment = Comment.objects.get(id=comment_id)
        new_reply = Reply.objects.create(comment=comment,
                                         body=reply)
        return redirect('book:book_detail', slug)
    else:
        return redirect('book:book_detail', slug)


def reply_list(request, slug):
    book = get_object_or_404(Book, slug=slug)
    replies = Reply.objects.filter(comment__book=book)
    return render(request, 'book/book_detail.html', {'replies': replies})