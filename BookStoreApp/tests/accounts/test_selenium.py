# import time
# from selenium import webdriver
# from django.test import LiveServerTestCase
# from selenium.webdriver.common.by import By
# import pytest
#
# class SignUpTest(LiveServerTestCase):
#
#     def setUp(self) -> None:
#         self.username = 'user-test'
#         self.email = 'user-email@emaple.com'
#         self.password = 'password'
#         self.password2 = 'password'
#         self.base_url = "http://127.0.0.1:8000/"
#         self.browser = webdriver.Chrome()
#
#     def tearDown(self) -> None:
#         self.browser.quit()
#
#     @pytest.mark.django_db
#     def test_should_sign_up_by_unique_username_email(self):
#
#         # get main page
#         self.browser.get(self.base_url)
#
#         # get sign up button
#         sign_up_button = self.browser.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div/ul/li[1]/a')
#         sign_up_button.click()
#
#         # set sign up values
#         username_field = self.browser.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[2]')
#         username_field.click()
#         username_field.send_keys(self.username)
#         time.sleep(1)
#         email_field = self.browser.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[3]')
#         email_field.click()
#         email_field.send_keys(self.email)
#         time.sleep(1)
#         password_field = self.browser.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[4]')
#         password_field.click()
#         password_field.send_keys(self.password)
#         time.sleep(1)
#         password2_field = self.browser.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/input[5]')
#         password2_field.click()
#         password2_field.send_keys(self.password2)
#
#         # get sign up button
#         bt = self.browser.find_element(By.XPATH, '//*[@id="form"]/div/div/div/form/button')
#         bt.click()
#         time.sleep(3)
#
#         # assertion
#         exit_bt = self.browser.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[5]/a')
#         self.assertIn('خروج', exit_bt.text)
#
#         username = self.browser.find_element(By.XPATH, '//*[@id="header"]/div/div/div[1]/div[2]/div/ul/li[1]/a')
#         self.assertIn(f'{self.username}', username.text)
#
