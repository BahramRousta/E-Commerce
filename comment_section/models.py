from django.db import models
from book.models import Book


class CommentSection(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comment')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.username


