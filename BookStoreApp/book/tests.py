import time
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By


class AdminTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_admin_site(self):
        self.browser.get("http://127.0.0.1:8000/admin/")
        time.sleep(1)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Django administration', body.text)


