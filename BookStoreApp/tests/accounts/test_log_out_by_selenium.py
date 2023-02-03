import time
from selenium.webdriver.common.by import By
from .test_log_in_by_selenium import TestLogInBySelenium


class TestLogOutBySelenium(TestLogInBySelenium):

    def test_logout(self):

        self.sign_in_step(username="admin", password="1")
        time.sleep(2)
        exit_bt = self.driver.find_element(By.XPATH, '//*[text()=" خروج "]')
        exit_bt.click()
        time.sleep(2)

        # assertion
        enter_bt = self.driver.find_element(By.XPATH, '//*[text()=" ورود "]')
        assert "ورود" in enter_bt.text
