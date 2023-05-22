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


class CreateReplyView(CreateView):
    model = Reply
    fields = ['body']

    def form_valid(self, form):
        comment_id = self.kwargs['comment_id']
        comment = Comment.objects.get(id=comment_id)
        form.instance.comment = comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book:book_detail', kwargs={'slug': self.kwargs['slug']})


class ReplyListView(ListView):
    model = Reply
    template_name = 'book/book_detail.html'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.filter(comment__book__slug=self.kwargs['slug']).all()
        return queryset