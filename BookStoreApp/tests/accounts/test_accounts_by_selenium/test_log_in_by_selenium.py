from faker import Faker
from selenium.webdriver.common.by import By
from tests.conftest import TestBaseConfig
fake = Faker()


class TestLogInBySelenium(TestBaseConfig):

    def sign_in_step(self, username, password):
        """
        @rtype: object
        """

        enter_button = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div/ul/li[2]/a')
        enter_button.click()

        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys(username)

        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        enter = self.driver.find_element(By.XPATH, '//button[text()="ورود"]')
        enter.click()

    def test_should_sign_in_successfully_with_valid_username_and_password(self):

        self.sign_in_step(username="admin", password="1")

        # assertion
        exit_bt = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[5]/a')
        assert 'خروج' in exit_bt.text

        username = self.driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[1]/a')
        assert "admin" in username.text

    def test_should_sign_in_failed_with_invalid_username_and_password(self):

        self.sign_in_step(
                          username="mock",
                          password="mock")

        error = self.driver.find_element(By.XPATH, '//*[@id="form"]/div[1]/div/h3')
        assert "اطلاعات وارد شده نامعتبر می باشد." in error.text
