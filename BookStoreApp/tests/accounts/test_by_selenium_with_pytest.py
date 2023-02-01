import time
import pytest
from faker import Faker
from selenium.webdriver.common.by import By

fake = Faker()


@pytest.mark.django_db
class TestSignUP:

    @pytest.mark.django_db
    def test_sign_up(self, driver):
        self.driver = driver
        self.username = fake.name()
        self.email = fake.email()
        self.password = 'password'
        self.password2 = 'password'

        driver.get("http://127.0.0.1:8000/")

        # get sign up button
        sign_up_button = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div/ul/li[1]/a')
        sign_up_button.click()

        # set sign up values
        username_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[2]')
        username_field.click()
        username_field.send_keys(self.username)
        time.sleep(1)
        email_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[3]')
        email_field.click()
        email_field.send_keys(self.email)
        time.sleep(1)
        password_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[4]')
        password_field.click()
        password_field.send_keys(self.password)
        time.sleep(1)
        password2_field = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[5]')
        password2_field.click()
        password2_field.send_keys(self.password2)

        # get sign up button
        bt = self.driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/button')
        bt.click()
        time.sleep(3)

        # assertion
        exit_bt = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[5]/a')
        assert 'خروج' in exit_bt.text

        username = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[1]/a')
        assert f'{self.username}' in username.text

        self.driver.quit()
