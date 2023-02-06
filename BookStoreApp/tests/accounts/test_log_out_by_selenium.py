import time
from selenium.webdriver.common.by import By
from tests.accounts.test_log_in_by_selenium import TestLogInBySelenium
from tests.conftest import TestBaseConfig


class TestLogOutBySelenium(TestBaseConfig):

    def test_logout(self):

        TestLogInBySelenium.sign_in_step(self, username="admin", password="1")
        time.sleep(2)
        exit_bt = self.driver.find_element(By.XPATH, '//*[text()=" خروج "]')
        exit_bt.click()
        time.sleep(2)

        # assertion
        enter_bt = self.driver.find_element(By.XPATH, '//*[text()=" ورود "]')
        assert "ورود" in enter_bt.text
