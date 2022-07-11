from django.urls import path
from .views import signup, signin, log_out

app_name = "register"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('log_out/', log_out, name='log_out'),
]