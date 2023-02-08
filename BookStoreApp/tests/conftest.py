import pytest
from django.test import Client
from django.utils import timezone
from selenium import webdriver
from django.contrib.auth.models import User
from faker import Faker
from taggit.models import Tag

from book.models import Publisher, Author, Category, Book

fake = Faker()


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def user():
    return User.objects.create_user(username="username",
                                    email="username@example.com",
                                    password='password')


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def publisher():
    return Publisher.objects.create(name="publisher",
                                    slug="publisher")


@pytest.fixture
def author():
    return Author.objects.create(name="author",
                                 slug="author")


@pytest.fixture()
def category():
    return Category.objects.create(name="category",
                                   slug="category")


@pytest.fixture()
def tag():
    return Tag.objects.create(name="tag")


@pytest.fixture()
def book(author, category, publisher, tag):
    book = Book.objects.create(title="book",
                               slug="book",
                               category=category,
                               publisher=publisher,
                               published=timezone.now(),
                               new_publish=True,
                               price=1000,
                               available=True,
                               tags=tag)
    book.author.add(author)
    book.save()
    return book


class TestBaseConfig:

    def setup_method(self) -> None:
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/"
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(15)

    def teardown_method(self) -> None:
        self.driver.quit()