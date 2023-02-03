import pytest
from django.test import Client
from selenium import webdriver
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def user(db):
    return User.objects.create_user(username=fake.name(),
                                    email=fake.email(),
                                    password='password')


@pytest.fixture
def client():
    return Client()