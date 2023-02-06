import time
import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium import webdriver


fake = Faker()


class TestSignUP:

    def setup_method(self):
        self.base_url = 'http://127.0.0.1:8000/'
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.get(self.base_url)

    # @pytest.mark.django_db
    def test_should_sign_up_successfully_by_selenium(self):

        username = fake.name()
        email = fake.email()
        password = 'password'
        password2 = 'password'

        self.driver.get(self.base_url)

        # get sign up button
        sign_up_button = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div/ul/li[1]/a')
        sign_up_button.click()

        # set sign up values
        username_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[2]')
        username_field.click()
        username_field.send_keys(username)
        time.sleep(1)
        email_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[3]')
        email_field.click()
        email_field.send_keys(email)
        time.sleep(1)
        password_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[4]')
        password_field.click()
        password_field.send_keys(password)
        time.sleep(1)
        password2_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[5]')
        password2_field.click()
        password2_field.send_keys(password2)

        # get sign up button
        bt = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/button')
        bt.click()
        time.sleep(3)

        # assertion
        exit_bt = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[5]/a')
        assert 'خروج' in exit_bt.text

        username_check = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[1]/a')
        assert username in username_check.text

    def teardown_method(self):
        self.driver.quit()