from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from book.models import Book


def comment(request, slug):
    book = get_object_or_404(Book, slug=slug)

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        body = request.POST['body']

        new_commnet = Comment.objects.create(username=username,
                                                    email=email,
                                                    body=body,
                                                    book=book)
        new_commnet.book = book
        new_commnet.save()
        return redirect('book:book_detail', slug)
    else:
        return redirect('book:book_detail', slug)


def comment_ist(request, slug):
    book = get_object_or_404(Book, slug=slug)
    comments = CommentSection.objects.filter(book=book)
    print(comments)
    return render(request, 'book/book_list_by_tag.html', {'comments': comments})