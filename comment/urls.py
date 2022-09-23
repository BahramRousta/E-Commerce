from django.urls import path
from .views import comment, comment_ist, reply_comment, reply_list

app_name = 'comment'

urlpatterns = [
    path('comment/<slug:slug>', comment, name='comment'),
    path('comment_list/<slug:slug>/', comment_ist, name='comment_ist'),
    path('reply_list/<slug:slug>/', reply_list, name='reply_list'),
    path('reply_comment/<int:comment_id>/<slug:slug>/', reply_comment, name='reply_comment'),
]