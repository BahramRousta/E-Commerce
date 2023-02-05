import pytest
from django.test import Client
from selenium import webdriver
from django.contrib.auth.models import User
from faker import Faker
from book.models import Publisher, Author, Category

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
