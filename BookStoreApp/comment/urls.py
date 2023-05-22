from django.urls import path
from .views import CommentCreateView, CommentListView, CreateReplyView, reply_list

app_name = 'comment'

urlpatterns = [
    path('comment/<slug:slug>', CommentCreateView.as_view(), name='comment'),
    path('comment_list/<slug:slug>/', CommentListView.as_view(), name='comment_ist'),
    path('reply_list/<slug:slug>/', reply_list, name='reply_list'),
    path('reply_comment/<int:comment_id>/<slug:slug>/', CreateReplyView.as_view(), name='reply_comment'),
]