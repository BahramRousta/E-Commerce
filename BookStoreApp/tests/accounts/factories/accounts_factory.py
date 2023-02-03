import factory
from django.db.models.signals import post_save
from factory import SubFactory
from faker import Faker
from django.contrib.auth.models import User
from accounts.models import Profile

fake = Faker()



@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory('app.factories.UserFactory', profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')