import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    return webdriver.Chrome()