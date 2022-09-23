from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Reply
from book.models import Book


def comment(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        body = request.POST['body']

        new_comment = Comment.objects.create(username=username,
                                             email=email,
                                             body=body,
                                             book=book)
        new_comment.book = book
        new_comment.save()
        return redirect('book:book_detail', slug)
    else:
        return redirect('book:book_detail', slug)


def comment_ist(request, slug):
    book = get_object_or_404(Book, slug=slug)
    comments = Comment.objects.filter(book=book)
    return render(request, 'book/book_list_by_tag.html', {'comments': comments})


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