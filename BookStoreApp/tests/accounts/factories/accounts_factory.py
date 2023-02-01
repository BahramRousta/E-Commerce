import factory
from faker import Faker
from django.contrib.auth.models import User

facke = Faker()

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

